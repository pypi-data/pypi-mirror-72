import json
import os
import logging
import pickle as pkl

from parsl.app.errors import RemoteExceptionWrapper

from fair_research_login import NativeClient, JSONTokenStorage
from funcx.serialize import FuncXSerializer
# from funcx.sdk.utils.futures import FuncXFuture
from funcx.sdk.utils import throttling
from funcx.sdk.utils.batch import Batch
from funcx.errors import MalformedResponse

logger = logging.getLogger(__name__)

class FuncXClient(throttling.ThrottledBaseClient):
    """Main class for interacting with the funcX service

    Holds helper operations for performing common tasks with the funcX service.
    """

    TOKEN_DIR = os.path.expanduser("~/.funcx/credentials")
    TOKEN_FILENAME = 'funcx_sdk_tokens.json'
    CLIENT_ID = '4cf29807-cf21-49ec-9443-ff9a3fb9f81c'

    def __init__(self, http_timeout=None, funcx_home=os.path.join('~', '.funcx'),
                 force_login=False, fx_authorizer=None, funcx_service_address='https://funcx.org/api/v1',
                 **kwargs):
        """ Initialize the client

        Parameters
        ----------
        http_timeout: int
        Timeout for any call to service in seconds.
        Default is no timeout

        force_login: bool
        Whether to force a login to get new credentials.

        fx_authorizer:class:`GlobusAuthorizer <globus_sdk.authorizers.base.GlobusAuthorizer>`:
        A custom authorizer instance to communicate with funcX.
        Default: ``None``, will be created.

        service_address: str
        The address of the funcX web service to communicate with.
        Default: https://dev.funcx.org/api/v1

        Keyword arguments are the same as for BaseClient.
        """
        self.func_table = {}
        self.ep_registration_path = 'register_endpoint_2'
        self.funcx_home = os.path.expanduser(funcx_home)

        if not os.path.exists(self.TOKEN_DIR):
            os.makedirs(self.TOKEN_DIR)

        tokens_filename = os.path.join(self.TOKEN_DIR, self.TOKEN_FILENAME)
        self.native_client = NativeClient(client_id=self.CLIENT_ID,
                                          app_name="FuncX SDK",
                                          token_storage=JSONTokenStorage(tokens_filename))

        fx_scope = "https://auth.globus.org/scopes/facd7ccc-c5f4-42aa-916b-a0e270e2c2a9/all"

        if not fx_authorizer:
            self.native_client.login(requested_scopes=[fx_scope],
                                     no_local_server=kwargs.get("no_local_server", True),
                                     no_browser=kwargs.get("no_browser", True),
                                     refresh_tokens=kwargs.get("refresh_tokens", True),
                                     force=force_login)

            all_authorizers = self.native_client.get_authorizers_by_scope(requested_scopes=[fx_scope])
            fx_authorizer = all_authorizers[fx_scope]

        super(FuncXClient, self).__init__("funcX",
                                          environment='funcx',
                                          authorizer=fx_authorizer,
                                          http_timeout=http_timeout,
                                          base_url=funcx_service_address,
                                          **kwargs)
        self.fx_serializer = FuncXSerializer()

    def logout(self):
        """Remove credentials from your local system
        """
        self.native_client.logout()

    def update_table(self, return_msg, task_id):
        """ Parses the return message from the service and updates the internal func_tables

        Parameters
        ----------

        return_msg : str
           Return message received from the funcx service
        task_id : str
           task id string
        """
        if isinstance(return_msg, str):
            r_dict = json.loads(return_msg)
        else:
            r_dict = return_msg

        status = {'pending': True}

        if 'result' in r_dict:
            try:
                r_obj = self.fx_serializer.deserialize(r_dict['result'])
            except Exception:
                raise Exception("Failure during deserialization of the result object")
            else:
                status.update({'pending': 'False',
                               'result': r_obj})
                self.func_table[task_id] = status

        elif 'exception' in r_dict:
            try:
                r_exception = self.fx_serializer.deserialize(r_dict['exception'])
                logger.info(f"Exception : {r_exception}")
            except Exception:
                raise Exception("Failure during deserialization of the Task's exception object")
            else:
                status.update({'pending': 'False',
                               'exception': r_exception})
                self.func_table[task_id] = status
        return status

    def get_task(self, task_id):
        """Get a funcX task.

        Parameters
        ----------
        task_id : str
            UUID of the task

        Returns
        -------
        dict
            Task block containing "status" key.
        """
        if task_id in self.func_table:
            return self.func_table[task_id]

        r = self.get("tasks/{task_id}".format(task_id=task_id))
        logger.debug("Response string : {}".format(r))
        try:
            rets = self.update_table(r.text, task_id)
        except Exception as e:
            raise e
        return rets

    def get_result(self, task_id):
        """ Get the result of a funcX task

        Parameters
        ----------
        task_id: str
            UUID of the task

        Returns
        -------
        Result obj: If task completed

        Raises
        ------
        Exception obj: Exception due to which the task failed
        """
        task = self.get_task(task_id)
        if task['pending'] is True:
            raise Exception("Task pending")
        else:
            if 'result' in task:
                return task['result']
            else:
                logger.warning("We have an exception : {}".format(task['exception']))
                task['exception'].reraise()

    def get_batch_status(self, task_id_list):
        """ Request status for a batch of task_ids
        """
        assert isinstance(task_id_list, list), "get_batch_status expects a list of task ids"

        pending_task_ids = [t for t in task_id_list if t not in self.func_table]

        results = {}

        if pending_task_ids :
            payload = {'task_ids': pending_task_ids}
            r = self.post("/batch_status", json_body=payload)
            logger.debug("Response string : {}".format(r))

        pending_task_ids = set(pending_task_ids)

        for task_id in task_id_list:
            if task_id in pending_task_ids:
                try:
                    data = r['results'][task_id]
                    rets = self.update_table(data, task_id)
                    results[task_id] = rets
                except KeyError:
                    logger.debug("Task {} info was not available in the batch status")
                except Exception as e:
                    logger.exception("Failure while unpacking results fom get_batch_status")
            else:
                results[task_id] = self.func_table[task_id]

        return results

    def get_batch_result(self, task_id_list):
        """ Request results for a batch of task_ids
        """
        pass

    def run(self, *args, endpoint_id=None, function_id=None, **kwargs):
        """Initiate an invocation

        Parameters
        ----------
        *args : Any
            Args as specified by the function signature
        endpoint_id : uuid str
            Endpoint UUID string. Required
        function_id : uuid str
            Function UUID string. Required
        asynchronous : bool
            Whether or not to run the function asynchronously

        Returns
        -------
        task_id : str
        UUID string that identifies the task
        """
        assert endpoint_id is not None, "endpoint_id key-word argument must be set"
        assert function_id is not None, "function_id key-word argument must be set"

        batch = self.create_batch()
        batch.add(*args, endpoint_id=endpoint_id, function_id=function_id, **kwargs)
        r = self.batch_run(batch)

        """
        Create a future to deal with the result
        funcx_future = FuncXFuture(self, task_id, async_poll)

        if not asynchronous:
            return funcx_future.result()

        # Return the result
        return funcx_future
        """

        return r[0]

    def create_batch(self):
        """
        Create a Batch instance to handle batch submission in funcX

        Parameters
        ----------

        Returns
        -------
        Batch instance
            Status block containing "status" key.
        """
        batch = Batch()
        return batch

    def batch_run(self, batch):
        """Initiate a batch of tasks to funcX

        Parameters
        ----------
        batch: a Batch object

        Returns
        -------
        task_ids : a list of UUID strings that identify the tasks
        """
        servable_path = 'submit'
        assert isinstance(batch, Batch), "Requires a Batch object as input"
        assert len(batch.tasks) > 0, "Requires a non-empty batch"

        data = batch.prepare()

        # Send the data to funcX
        r = self.post(servable_path, json_body=data)
        if r.http_status is not 200:
            raise Exception(r)

        if 'task_uuids' not in r:
            raise MalformedResponse(r)

        return r['task_uuids']

    def map_run(self, *args, endpoint_id=None, function_id=None, asynchronous=False, **kwargs):
        """Initiate an invocation

        Parameters
        ----------
        *args : Any
            Args as specified by the function signature
        endpoint_id : uuid str
            Endpoint UUID string. Required
        function_id : uuid str
            Function UUID string. Required
        asynchronous : bool
            Whether or not to run the function asynchronously

        Returns
        -------
        task_id : str
        UUID string that identifies the task
        """
        servable_path = 'submit_batch'
        assert endpoint_id is not None, "endpoint_id key-word argument must be set"
        assert function_id is not None, "function_id key-word argument must be set"

        ser_kwargs = self.fx_serializer.serialize(kwargs)

        batch_payload = []
        iterator = args[0]
        for arg in iterator:
            ser_args = self.fx_serializer.serialize((arg,))
            payload = self.fx_serializer.pack_buffers([ser_args, ser_kwargs])
            batch_payload.append(payload)

        data = {'endpoints': [endpoint_id],
                'func': function_id,
                'payload': batch_payload,
                'is_async': asynchronous}

        # Send the data to funcX
        r = self.post(servable_path, json_body=data)
        if r.http_status is not 200:
            raise Exception(r)

        if 'task_uuids' not in r:
            raise MalformedResponse(r)

        return r['task_uuids']


    def register_endpoint(self, name, endpoint_uuid, description=None):
        """Register an endpoint with the funcX service.

        Parameters
        ----------
        name : str
            Name of the endpoint
        endpoint_uuid : str
                The uuid of the endpoint
        description : str
            Description of the endpoint

        Returns
        -------
        A dict
            {'endopoint_id' : <>,
             'address' : <>,
             'client_ports': <>}
        """
        data = {"endpoint_name": name, "endpoint_uuid": endpoint_uuid, "description": description}

        r = self.post(self.ep_registration_path, json_body=data)
        if r.http_status is not 200:
            raise Exception(r)

        # Return the result
        return r.data

    def get_containers(self, name, description=None):
        """Register a DLHub endpoint with the funcX service and get the containers to launch.

        Parameters
        ----------
        name : str
            Name of the endpoint
        description : str
            Description of the endpoint

        Returns
        -------
        int
            The port to connect to and a list of containers
        """
        registration_path = 'get_containers'

        data = {"endpoint_name": name, "description": description}

        r = self.post(registration_path, json_body=data)
        if r.http_status is not 200:
            raise Exception(r)

        # Return the result
        return r.data['endpoint_uuid'], r.data['endpoint_containers']

    def get_container(self, container_uuid, container_type):
        """Get the details of a container for staging it locally.

        Parameters
        ----------
        container_uuid : str
            UUID of the container in question
        container_type : str
            The type of containers that will be used (Singularity, Shifter, Docker)

        Returns
        -------
        dict
            The details of the containers to deploy
        """
        container_path = f'containers/{container_uuid}/{container_type}'

        r = self.get(container_path)
        if r.http_status is not 200:
            raise Exception(r)

        # Return the result
        return r.data['container']

    def get_endpoint_status(self, endpoint_uuid):
        """Get the status reports for an endpoint.

        Parameters
        ----------
        endpoint_uuid : str
            UUID of the endpoint in question

        Returns
        -------
        dict
            The details of the endpoint's stats
        """
        stats_path = f'endpoints/{endpoint_uuid}/status'

        r = self.get(stats_path)
        if r.http_status is not 200:
            raise Exception(r)

        # Return the result
        return r.data

    def register_function(self, function, function_name=None, container_uuid=None, description=None,
                          public=False, group=None):
        """Register a function code with the funcX service.

        Parameters
        ----------
        function : Python Function
            The function to be registered for remote execution
        function_name : str
            The entry point (function name) of the function. Default: None
        container_uuid : str
            Container UUID from registration with funcX
        description : str
            Description of the file
        public : bool
            Whether or not the function is publicly accessible. Default = False
        group : str
            A globus group uuid to share this function with

        Returns
        -------
        function uuid : str
            UUID identifier for the registered function
        """
        registration_path = 'register_function'

        serialized_fn = self.fx_serializer.serialize(function)
        packed_code = self.fx_serializer.pack_buffers([serialized_fn])

        data = {"function_name": function.__name__,
                "function_code": packed_code,
                "container_uuid": container_uuid,
                "entry_point": function_name if function_name else function.__name__,
                "description": description,
                "public": public,
                "group": group}

        logger.info("Registering function : {}".format(data))

        r = self.post(registration_path, json_body=data)
        if r.http_status is not 200:
            raise Exception(r)

        # Return the result
        return r.data['function_uuid']

    def register_container(self, location, container_type, name='', description=''):
        """Register a container with the funcX service.

        Parameters
        ----------
        location : str
            The location of the container (e.g., its docker url). Required
        container_type : str
            The type of containers that will be used (Singularity, Shifter, Docker). Required

        name : str
            A name for the container. Default = ''
        description : str
            A description to associate with the container. Default = ''

        Returns
        -------
        str
            The id of the container
        """
        container_path = f'containers'

        payload = {'name': name, 'location': location, 'description': description, 'type': container_type}

        r = self.post(container_path, json_body=payload)
        if r.http_status is not 200:
            raise Exception(r)

        # Return the result
        return r.data['container_id']

    def add_to_whitelist(self, endpoint_id, function_ids):
        """Adds the function to the endpoint's whitelist

        Parameters
        ----------
        endpoint_id : str
            The uuid of the endpoint
        function_ids : list
            A list of function id's to be whitelisted

        Returns
        -------
        json
            The response of the request
        """
        req_path = f'endpoints/{endpoint_id}/whitelist'

        if not isinstance(function_ids, list):
            function_ids = [function_ids]

        payload = {'func': function_ids}

        r = self.post(req_path, json_body=payload)
        if r.http_status is not 200:
            raise Exception(r)

        # Return the result
        return r

    def get_whitelist(self, endpoint_id):
        """List the endpoint's whitelist

        Parameters
        ----------
        endpoint_id : str
            The uuid of the endpoint

        Returns
        -------
        json
            The response of the request
        """
        req_path = f'endpoints/{endpoint_id}/whitelist'

        r = self.get(req_path)
        if r.http_status is not 200:
            raise Exception(r)

        # Return the result
        return r

    def delete_from_whitelist(self, endpoint_id, function_ids):
        """List the endpoint's whitelist

        Parameters
        ----------
        endpoint_id : str
            The uuid of the endpoint
        function_ids : list
            A list of function id's to be whitelisted

        Returns
        -------
        json
            The response of the request
        """
        if not isinstance(function_ids, list):
            function_ids = [function_ids]
        res = []
        for fid in function_ids:
            req_path = f'endpoints/{endpoint_id}/whitelist/{fid}'

            r = self.delete(req_path)
            if r.http_status is not 200:
                raise Exception(r)
            res.append(r)

        # Return the result
        return res
