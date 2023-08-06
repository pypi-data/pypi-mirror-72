# -*- coding:utf-8 -*-
import os

from . import defaults
from . import exceptions
from . import http
from . import yml_utils
from . import version
from .compat import urlparse
from .models import *


def _normalize_endpoint(endpoint):
    if not endpoint.startswith('http://') and not endpoint.startswith('https://'):
        return 'https://' + endpoint
    else:
        return endpoint


_SUPPORTED = ['gwl', 'wdl']


class _Base(object):
    def __init__(self, auth, endpoint, connect_timeout):
        self.session = http.Session()
        self.auth = auth
        self.endpoint = _normalize_endpoint(endpoint)
        self.timeout = defaults.get(connect_timeout, defaults.connect_timeout)

    def _do(self, method, res_account_name, project_name, target, **kwargs):
        target = to_string(target)
        content_type = kwargs.pop('content_type', None)
        make_url = _UrlMaker(self.endpoint, kwargs.pop('operation'))
        self.data = kwargs.pop('data', None)
        self.params = kwargs.pop('params', None)

        files = kwargs.pop('files', None)
        req = http.Request(
            method, self.auth, make_url(res_account_name, project_name, target, **kwargs),
            content_type=content_type,
            files=files,
            data=self.data,
            params=self.params,
            headers={"User-Agent": "gdpy/%s" % version.__version__}
        )

        resp = self.session.do_request(req, timeout=self.timeout)
        if resp.status // 100 != 2:
            raise exceptions.make_exception(resp)

        return resp

    @staticmethod
    def _parse_result(resp, parse_func, klass):
        result = klass(resp)
        parse_func(result, resp.response.content)
        return result

    def _get_url(self, res_account_name, res_project_name, target, **kwargs):
        make_url = _UrlMaker(self.endpoint, kwargs.pop('operation'))
        return make_url(res_account_name, res_project_name, target, **kwargs)


class _UrlMaker(object):

    def __init__(self, endpoint, operation):
        p = urlparse(endpoint)

        self.scheme = p.scheme
        self.netloc = p.netloc
        self.operation = operation

    def __call__(self, res_account_name, res_project_name, target, **kwargs):
        self.project_name = res_project_name
        self.account_name = res_account_name
        end_slash = kwargs.pop('end_slash', 1)
        if target:
            if not len(kwargs):
                url = '{0}://{1}/accounts/{2}/projects/{3}/{4}/{5}/'.format(self.scheme, self.netloc,
                                                                            self.account_name, self.project_name,
                                                                            self.operation, target)
                if end_slash == 0:
                    return url[:-1]
                else:
                    return url
            else:
                params = list()
                for item in kwargs:
                    if kwargs.get(item):
                        params.append(item + '=' + str(kwargs.get(item)))
                parameters = '?' + '&'.join(params)
                return '{0}://{1}/accounts/{2}/projects/{3}/{4}/{5}/{6}'.format(self.scheme, self.netloc,
                                                                                self.account_name, self.project_name,
                                                                                self.operation, target, parameters)
        else:
            return '{0}://{1}/accounts/{2}/projects/{3}/{4}/'.format(self.scheme, self.netloc, self.account_name,
                                                                     self.project_name, self.operation)


class Tasks(_Base):
    """ 用于Tasks操作的类
    :param auth: 包含了用户认证信息的Auth对象
    :type auth: gdpy.GeneDockAuth

    :param str endpoint: 访问域名，如北京区域的域名为cn-beijing-api.genedock.com
    :param str res_account_name: 指定从该账号下获取资源(如需获取公共资源，则为public)
    :param str project_name: 指定从该项目下获取资源(默认为default)
    :raises: 如果获取或上传失败，则抛出来自服务端的异常; 还可能抛出其他异常
    tasks related operations
    usage::
        >>> import gdpy
        >>> auth = gdpy.GeneDockAuth('access_key_id', 'access_key_secret')
        >>> task = gdpy.Tasks(auth, 'https://cn-beijing-api.genedock.com', 'res_account_name', 'project_name')
    """

    def __init__(self, auth, endpoint, res_account_name, project_name='default', connect_timeout=None, task_type='gwl'):
        super(Tasks, self).__init__(auth, endpoint, connect_timeout)
        self.res_account_name = res_account_name
        self.res_project_name = project_name
        self._task_type = str(task_type).lower()

        if self._task_type not in _SUPPORTED:
            raise NotImplementedError("Unsupported task type '{}'".format(self._task_type))

    def __do_task(self, method, id=None, **kwargs):
        return self._do(method, self.res_account_name, self.res_project_name, id, **kwargs)

    @property
    def operation(self):
        if self._task_type == 'gwl':
            return 'tasks'
        elif self._task_type == 'wdl':
            return 'wdl/tasks'
        return None

    def get_task(self, id):
        """
        usage:
            >>> resp = task.get_task('task_id')
        """
        resp = self.__do_task('GET', id, operation=self.operation)
        return GetTaskResult(resp)

    def list_tasks(self, **kwargs):
        """
        usage:
            >>> resp = task.list_tasks()
        """
        default_to = int(time.time())
        default_from = default_to - 60 * 60 * 24 * 7
        params = {'from': default_from, 'to': default_to}
        if 'params' in list(kwargs.keys()):
            if kwargs['params'].get('from'):
                kwargs['params']['from'] = int(kwargs['params']['from'])
            if kwargs['params'].get('to'):
                kwargs['params']['to'] = int(kwargs['params']['to'])
            resp = self.__do_task('GET', operation=self.operation, **kwargs)
        else:
            resp = self.__do_task('GET', params=params, operation=self.operation, **kwargs)
        return self._parse_result(resp, yml_utils.parse_list_tasks, ListTasksResult)

    def create_task(self, workflow_name_or_id, workflow_version, parameters, **kwargs):
        """
        create a task by workflow
            1. create a gwl task: tasks.create_task("WF_Name", 1, parameters={...}, owner="WF_Owner")
            2. create a wdl task: tasks.create_task("WF_ID", 1, parammeters={"inputs": [], "output_dir": "/path..."})

        :param workflow_name_or_id:
        :param workflow_version:
        :param parameters:
        :param kwargs:
        :return:
        """

        if self._task_type == 'gwl':
            data = {
                "parameters": parameters,
                "workflow_name": workflow_name_or_id,
                "workflow_version": int(workflow_version),
                "workflow_owner": kwargs.get('owner') or self.res_account_name,
                "task_name": parameters.get('name')
            }
        elif self._task_type == 'wdl':
            data = {
                "workflow_id": workflow_name_or_id,
                "workflow_version": workflow_version,
                "inputs": parameters.get("inputs"),
                "output_dir": parameters.get("output_dir"),
                "task_name": parameters.get('name')
            }
        else:
            data = {}
        resp = self.__do_task('POST', '', data=data, operation=self.operation)
        return ActiveWorkflowResult(resp)

    def active_workflow(self, param_file, workflow_name, workflow_version, workflow_owner=None):
        """ create a task by gwl (workflow name and workflow version) or wdl (workflow id) from `parameters file`
        usage::
            >>> resp = task.active_workflow('workflow_param_file', 'workflow_name', 'workflow_version')
        """
        if not workflow_owner:
            workflow_owner = self.res_account_name
        if not is_object_name_valid(workflow_name):
            raise ValueError(
                "Invalid workflow name! Expect a string started with "
                "alphabet and under 128 characters, but got {}!".format(str(workflow_name)))
        if not is_object_version_valid(workflow_version):
            raise ValueError(
                "Invalid workflow version! Expect "
                "interger greater than 0, but got {}".format(str(workflow_version)))
        try:
            parameters = yml_utils.yaml_loader(param_file)
            return self.create_task(
                workflow_name_or_id=workflow_name,
                workflow_version=workflow_version,
                parameters=parameters,
                owner=workflow_owner
            )
        except ValueError as e:
            raise e

    def delete_task(self, id):
        """
        usage:
            >>> resp = task.delete_task('task_id')
        """
        resp = self.__do_task('DELETE', id, operation=self.operation)
        return DeleteTaskResult(resp)

    def stop_task(self, id):
        """
        usage:
            >>> resp = task.stop_task('task_id')
        """
        resp = self.__do_task('PUT', id, operation=self.operation)
        return StopTaskResult(resp)

    def restart_task(self, id):
        """
        usage
             >>> resp = task.restart_task('task_id')
        """
        target = id + '/restart'
        resp = self.__do_task('PUT', target, operation=self.operation)
        return RestartTaskResult(resp)

    def get_jobs(self, id):
        """
        :rtype: gdpy.models.GetJobResult
        usage:
            >>> resp = task.get_jobs('task_id')
        """
        target = id + '/jobs'
        resp = self.__do_task('GET', target, operation=self.operation)
        return self._parse_result(resp, yml_utils.parse_get_jobs, GetJobResult)  # type: GetJobResult

    def get_job_cmd(self, id):
        """
        usage:
            >>> resp = task.get_job_cmd('job_id')
        """
        if self._task_type == 'wdl':
            raise NotImplementedError("Unsupported to get the cmd of a '{}' type job".format(self._task_type))
        task_id = id.split('_')[0]
        target = task_id + '/cmd/' + id
        resp = self.__do_task('GET', target, operation='tasks')
        return GetJobCmdResult(resp)

    def get_job_info(self, id):
        """
        usage:
            >>> resp = task.get_job_info('job_id')
        """
        task_id = id.split('_')[0]
        target = task_id + '/jobs/' + id
        resp = self.__do_task('GET', target, operation='tasks')
        return GetJobInfoResult(resp)


class Workflows(_Base):
    """ 用于Workflows操作的类
    :param auth: 包含了用户认证信息的Auth对象
    :type auth: gdpy.GeneDockAuth

    :param str endpoint: 访问域名，如北京区域的域名为cn-beijing-api.genedock.com
    :param str res_account_name: 指定从该账号下获取资源(如需获取公共资源，则为public)
    :param str project_name: 指定从该项目下获取资源(默认为default)
    :raises: 如果获取或上传失败，则抛出来自服务端的异常; 还可能抛出其他异常
    workflows related operations
    usage::
        >>> import gdpy
        >>> auth = gdpy.GeneDockAuth('access_key_id', 'access_key_secret')
        >>> workflow = gdpy.Workflows(auth, 'https://cn-beijing-api.genedock.com', 'res_account_name', 'project_name')
    """

    def __init__(
            self, auth, endpoint, res_account_name, project_name='default', connect_timeout=None, workflow_type='gwl'
    ):
        super(Workflows, self).__init__(auth, endpoint, connect_timeout)
        self.res_account_name = res_account_name
        self.res_project_name = project_name
        self._workflow_type = str(workflow_type).lower()

        if self._workflow_type not in _SUPPORTED:
            raise NotImplementedError("Unsupported workflow type '{}'".format(self._workflow_type))

    @property
    def operation(self):
        wf_type = self._workflow_type or 'gwl'
        if wf_type == 'wdl':
            return "wdl/workflow"
        elif wf_type == 'gwl':
            return "workflows"
        return None

    def __do_workflow(self, method, name=None, version=None, **kwargs):
        if name is not None and not is_object_name_valid(name):
            raise ValueError(
                "Invalid workflow name! Expect a string started with alphabet"
                " and under 128 characters, but got {}!".format(name)
            )
        if version is not None and not is_object_version_valid(version):
            raise ValueError(
                "Invalid workflow version! Expect interger greater than 0, but got {}".format(version)
            )
        return self._do(method, self.res_account_name, self.res_project_name, name, workflow_version=version, **kwargs)

    def _parse_list_workflows(self, *args, **kwargs):
        return yml_utils.parse_list_workflows(workflow_type=self._workflow_type, *args, **kwargs)

    @staticmethod
    def __close_files(*args):
        for fp in args:
            if fp:
                try:
                    fp.close()
                except IOError:
                    pass

    def list_workflows(self):
        """
        usage:
            >>> resp = workflow.list_workflows()
        :rtype: ListWorkflowsResult
        """
        resp = self.__do_workflow('GET', operation=self.operation)
        return self._parse_result(resp, self._parse_list_workflows, ListWorkflowsResult)

    def list_exc_workflows(self):
        """
        List executable workflow

        usage:
            >>> resp = workflow.list_exc_workflows()
        """
        if self._workflow_type == 'gwl':
            operation = 'executable-workflows'
        else:
            operation = self.operation
        resp = self.__do_workflow('GET', operation=operation)
        return self._parse_result(resp, self._parse_list_workflows, ListWorkflowsResult)

    def get_workflow(self, name, version=None):
        """
        :param name: workflow identify (gwl workflow name or wdl workflow id)
        :param version: workflow version
        usage:
            >>> resp = workflow.get_workflow('workflow_name_or_id', 'workflow_version')
            */Or lack version/*
            >>> resp = workflow.get_workflow('workflow_name_or_id')

        """
        if name is None:
            raise ValueError("Expect a name(str) started with alphabet and under 128 characters")
        resp = self.__do_workflow('GET', name, version, operation=self.operation)
        return GetWorkflowResult(resp)

    def get_exc_workflow(self, name, version):
        """
        :param name: workflow identify (gwl workflow name or wdl workflow id)
        :param version: workflow version
        usage:
            >>> resp = workflow.get_exc_workflow('workflow_name', 'workflow_version')
        get a yaml tempalte:
            >>> from gdpy.yml_utils import yaml_dumper
            >>> yml_template = yaml_dumper(resp.parameter)
        """
        if name is None:
            raise ValueError("Expect a name(str) started with alphabet and under 128 characters")
        if version is None:
            raise ValueError("Expect interger greater than 0 as version")
        resp = self.__do_workflow('GET', name, version, operation='executable-workflows')
        return GetExcWorkflowResult(resp)

    def delete_workflow(self, name, version):
        """
        :param name: workflow identify (gwl workflow name or wdl workflow id)
        :param version: workflow version
        usage:
            >>> resp = workflow.delete_workflow('workflow_name_or_id', 'workflow_version')
        """
        if name is None:
            raise ValueError("Expect a name(str) started with alphabet and under 128 characters")
        if version is None:
            raise ValueError("Expect interger greater than 0 as version")
        resp = self.__do_workflow('DELETE', name, version, operation=self.operation)
        return DeleteWorkflowResult(resp)

    def create_workflow(self, name, version=None, description='', attachment=None):
        """
        :param name: workflow identify (gwl workflow name or wdl workflow id)
        :param version: workflow version (not recommended)
        :param description: workflow description
        :param attachment: a dict with attributes `source_file` and `dependencies_zip`,
                        which specified the files need to upload
        usage:
            1. create normal workflow
            >>> resp = workflow.create_workflow('workflow_name', description='description')
            >>> print(resp.workflow_identify)  # workflow_identify == workflow_name
            2. create wdl workflow
            >>> resp = workflow.create_workflow('workflow_name', description='description', attachment={"source_file": "file_path"})
        """
        if not is_object_name_valid(name):
            raise ValueError(
                "Invalid workflow name! Expect a string started with alphabet "
                "and under 128 characters, but got {}!".format(str(name)))
        if version and not is_object_version_valid(version):
            raise ValueError(
                "Invalid workflow version! Expect "
                "interger greater than 0, but got {}".format(str(version)))

        attachment = attachment or {}

        def _create_normal_workflow():
            data = {"workflow_name": name, "workflow_version": version, "description": description}
            if not version:
                data.pop("workflow_version")
            resp = self.__do_workflow('POST', data=data, operation=self.operation)
            return CreateWorkflowResult(resp)

        def _create_wdl_workflow():

            self._check_workflow_attachment(attachment)

            dependencies = (
                open(attachment.get('dependencies_zip'), 'rb')
                if attachment.get('dependencies_zip') else None
            )
            source = open(attachment.get('source_file'), 'rb')
            try:
                data = {"name": name, "description": description}
                files = {"source": source} if not dependencies else {"source": source, "dependencies": dependencies}
                resp = self.__do_workflow(
                    'POST', data=data, files=files, operation=self.operation, content_type="multipart/form-data"
                )
                return CreateWorkflowResult(resp)
            finally:
                self.__close_files(source, dependencies)

        if self._workflow_type == 'gwl':
            result = _create_normal_workflow()
            result.workflow_identify = name
        elif self._workflow_type == 'wdl':
            result = _create_wdl_workflow()
            result.workflow_identify = result.response.json()['id']
        else:
            raise NotImplementedError("Unsupported workflow type '{}'".format(self._workflow_type))

        return result

    def get_workflow_info_by_name(self, name, version=None):
        if self._workflow_type != 'wdl':
            resp = self.get_workflow(name, version)
            return resp.response.json()
        resp = self.__do_workflow(
            'GET',
            operation=self.operation,
            version=version,
            params={
                "name": name,
                "version": version
            }
        )
        list_result = self._parse_result(resp, self._parse_list_workflows, ListWorkflowsResult)
        if not list_result.workflows:
            raise exceptions.ServerError(
                status=404,
                headers={},
                error_message="The workflow {} of version {} does not found!".format(name, version),
                error_message_chs="无法找到工作流: {} (版本号: {})".format(name, version),
                error_code="NotFound",
            )
        return list_result.workflows

    @staticmethod
    def _check_workflow_attachment(attachment, check_source=True):
        if check_source and not os.path.exists(attachment.get('source_file')):
            raise ValueError(
                "Expected a source_file(string) to specify the WDL file path, the file path must be existing"
            )

        if attachment.get('dependencies_zip') and not os.path.exists(attachment.get('source_file')):
            raise ValueError(
                "Local file path not found: {}".format(attachment.get('dependencies_zip'))
            )

    def update_workflow(self, name_or_id, version, **kwargs):
        """
        :param str name_or_id: workflow identify (gwl workflow name or wdl workflow id)
        :param version: workflow version (not recommended)
        :keyword description: new description
        :keyword configs: configs for GWL workflow
        :keyword attachment: attachment files for WDL workflow, i.e. {
                                "source_path": "/path/to/source", "dependencies_zip": "/path/to/dependencies"
                            }
        :keyword name: new workflow name for WDL workflow
        :keyword override: overwrite current version (default: true)
        """

        description = kwargs.get('description')
        result = None
        if self._workflow_type == 'gwl':
            try:
                data = dict()
                data["workflow_version"] = version
                data["configs"] = kwargs.get('configs')
                if description:
                    data["description"] = description
                resp = self.__do_workflow('PUT', name_or_id, data=data, operation=self.operation)
            except ValueError as e:
                raise e
            result = PutWorkflowResult(resp)
        elif self._workflow_type == 'wdl':
            data = {"workflow_version": version, "override": kwargs.get('override', True)}
            if kwargs.get('name'):
                data['name'] = kwargs['name']
            if description:
                data["description"] = description

            files = {}
            attachment = kwargs.get('attachment', {})
            if attachment:
                self._check_workflow_attachment(attachment, attachment.get('source_file'))
            if attachment.get('source_file'):
                files['source'] = open(attachment['source_file'], 'rb')
            if attachment.get('dependencies_zip'):
                files['dependencies'] = open(attachment['dependencies_zip'], 'rb')
            if kwargs.get('include_empty_imports') and not files.get('dependencies'):
                data['dependencies'] = None
            try:
                resp = self.__do_workflow(
                    'PUT', name_or_id, data=data, files=files, operation=self.operation,
                    content_type='multipart/form-data'
                )
                result = PutWorkflowResult(resp)
            finally:
                self.__close_files(files.get('source'), files.get('dependencies'))
        return result

    def put_workflow(self, param_file):
        """
        usage:
            >>> resp = workflow.put_workflow('parameter_file_path')
        """
        if self._workflow_type != "gwl":
            raise NotImplementedError(
                "Unsupported operation 'put_workflow' for '{}' type workflow".format(self._workflow_type))

        workflow_temp = yml_utils.yaml_loader(param_file)
        workflow_description = workflow_temp.get('workflow').get('description', '')
        if not is_object_name_valid(workflow_temp.get('workflow').get('name')):
            raise ValueError(
                "Invalid workflow name! Expect a string started with alphabet"
                " and under 128 characters, but got {}!".format(str(workflow_temp.get('workflow').get('name'))))
        else:
            workflow_name = str(workflow_temp.get('workflow').get('name'))
        if not is_object_version_valid(workflow_temp.get('workflow').get('version')):
            raise ValueError("Invalid tool version! Expect interger greater than 0, but got {}".format(
                str(workflow_temp.get('workflow').get('version'))))
        else:
            workflow_version = int(workflow_temp.get('workflow').get('version'))
        workflow_configs = {'nodelist': workflow_temp.get('workflow').get('nodelist')}
        return self.update_workflow(
            name_or_id=workflow_name,
            version=workflow_version,
            configs=workflow_configs,
            description=workflow_description
        )

    def set_workflow_param(self, param_file, name, version):
        """
        usage:
            >>> resp = workflow.set_workflow_param('exec_workflow_param_file', 'workflow_name', 'workflow_version')
        """
        if self._workflow_type != 'gwl':
            raise NotImplementedError(
                'Unable to set the workflow param for the "{}"type workflow'.format(self._workflow_type)
            )
        if not is_object_name_valid(name):
            raise ValueError(
                "Invalid workflow name! Expect a string started with "
                "alphabet and under 128 characters, but got {}!".format(str(name)))
        if not is_object_version_valid(version):
            raise ValueError(
                "Invalid workflow version! Expect interger greater than 0, but got {}".format(str(version))
            )
        workflow_temp = yml_utils.yaml_loader(param_file)
        data = {'workflow_version': version, 'parameters': workflow_temp}
        resp = self.__do_workflow('PUT', name, data=data, operation='executable-workflows')
        return SetWorkflowParamResult(resp)


class Tools(_Base):
    """ 用于Tools操作的类
    NOTE:
        不支持WDL工作流相关操作
    :param auth: 包含了用户认证信息的Auth对象
    :type auth: gdpy.GeneDockAuth

    :param str endpoint: 访问域名，如北京区域的域名为cn-beijing-api.genedock.com
    :param str res_account_name: 指定从该账号下获取资源(如需获取公共资源，则为public)
    :param str project_name: 指定从该项目下获取资源(默认为default)
    :raises: 如果获取或上传失败，则抛出来自服务端的异常; 还可能抛出其他异常
    tools related operations
    usage::
        >>> import gdpy
        >>> auth = gdpy.GeneDockAuth('access_key_id', 'access_key_secret')
        >>> tool = gdpy.Tools(auth, 'https://cn-beijing-api.genedock.com', 'res_account_name', 'project_name')
    """

    def __init__(self, auth, endpoint, res_account_name, project_name='default', connect_timeout=None):
        super(Tools, self).__init__(auth, endpoint, connect_timeout)
        self.res_account_name = res_account_name
        self.res_project_name = project_name

    def __do_tool(self, method, name=None, version=None, **kwargs):
        if name is not None and not is_object_name_valid(name):
            raise ValueError(
                "Invalid tool name! Expect a string started with "
                "alphabet and under 128 characters, but got {}!".format(str(name))
            )
        if version is not None and not is_object_version_valid(version):
            raise ValueError("Invalid tool version! Expect interger greater than 0, but got {}".format(str(version)))
        return self._do(method, self.res_account_name, self.res_project_name, name, tool_version=version, **kwargs)

    def get_tool(self, name, version=None):
        """
        usage:
            >>> resp = tool.get_tool('tool_name', 'tool_version')
            */Or lack version/*
            >>> resp = tool.get_tool('tool_name')
        """
        if name is None:
            raise ValueError("Expect a name(str) started with alphabet and under 128 characters")
        resp = self.__do_tool('GET', name, version, operation='tools')
        return GetToolResult(resp)

    def list_tools(self):
        """
        usage:
            >>> resp = tool.list_tools()
        """
        resp = self.__do_tool('GET', operation='tools')
        return self._parse_result(resp, yml_utils.parse_list_tools, ListToolResult)

    def get_tool_param(self, name, version=None):
        """
        usage:
            >>> resp = tool.get_tool_param('tool_name', 'tool_version')
            */Or lack version/*
            >>> resp = tool.get_tool_param('tool_name')
        """
        if name is None:
            raise ValueError("Expect a name(str) started with alphabet and under 128 characters")
        resp = self.__do_tool('GET', name, version, operation='toolparameters')
        return self._parse_result(resp, yml_utils.parse_get_tool_parameters, GetToolParamResult)

    def delete_tool(self, name, version):
        """
        usage:
            >>> resp = tool.delete_tool('tool_name', 'tool_version')
        """
        if name is None:
            raise ValueError("Expect a name(str) started with alphabet and under 128 characters")
        if version is None:
            raise ValueError("Expect interger greater than 0 as version")
        resp = self.__do_tool('DELETE', name, version, operation='tools')
        return DeleteToolResult(resp)

    def create_tool(self, name, version, description=''):
        """
        usage:
            >>> resp = tool.create_tool('tool_name', 'tool_version', 'description')
        """
        if not is_object_name_valid(name):
            raise ValueError(
                "Invalid tool name! Expect a string started with alphabet"
                " and under 128 characters, but got {}!".format(str(name))
            )
        if not is_object_version_valid(version):
            raise ValueError("Invalid tool version! Expect interger greater than 0, but got {}".format(str(version)))
        data = {"tool_name": name, "tool_version": version, "description": description}
        resp = self.__do_tool('POST', data=data, operation='tools')
        return CreateToolResult(resp)

    def put_tool(self, param_file):
        """
        usage:
            >>> resp = tool.put_tool('parameter_file_path')
        """
        tool_temp = yml_utils.yaml_loader(param_file)
        tool_description = tool_temp.get('app').get('description', '')
        if not is_object_name_valid(tool_temp.get('app').get('name')):
            raise ValueError(
                "Invalid tool name! Expect a string started with alphabet"
                " and under 128 characters, but got {}!".format(None))
        else:
            tool_name = str(tool_temp.get('app').get('name'))
        if not is_object_version_valid(tool_temp.get('app').get('version')):
            raise ValueError(
                "Invalid tool version! Expect interger greater than 0, but got {}".format(None)
            )
        else:
            tool_version = int(tool_temp.get('app').get('version'))
        tool_configs = tool_temp.get('app')
        try:
            data = dict()
            data["tool_version"] = tool_version
            data["configs"] = tool_configs
            data["description"] = tool_description
            resp = self.__do_tool('PUT', tool_name, data=data, operation='tools')
        except ValueError as e:
            raise e
        return PutToolResult(resp)


class Data(_Base):
    """ 用于Data操作的类
    :param auth: 包含了用户认证信息的Auth对象
    :type auth: gdpy.GeneDockAuth

    :param str endpoint: 访问域名，如北京区域的域名为cn-beijing-api.genedock.com
    :param str res_account_name: 指定从该账号下获取资源(如需获取公共资源，则为public)
    :param str project_name: 指定从该项目下获取资源(默认为default)
    :raises: 抛出异常
    data related operations
    usage::
        >>> import gdpy
        >>> auth = gdpy.GeneDockAuth('access_key_id', 'access_key_secret')
        >>> data = gdpy.Data(auth, 'https://cn-beijing-api.genedock.com', 'res_account_name', 'project_name')
    """

    def __init__(self, auth, endpoint, res_account_name, project_name='default', connect_timeout=None):
        super(Data, self).__init__(auth, endpoint, connect_timeout)
        self.res_account_name = res_account_name
        self.res_project_name = project_name

    def __do_data(self, method, data_path=None, **kwargs):
        return self._do(method, self.res_account_name, self.res_project_name, data_path, **kwargs)

    def archive_data(self, data_path=None):
        """
        usage:
            >>> resp = data.archive_data('data_path')
        """
        if data_path is None:
            raise ValueError("Expect a date path")
        resp = self.__do_data('POST', data_path, operation='archive', end_slash=0)
        return ArchiveDataResult(resp)

    def restore_data(self, data_path=None):
        """
        usage:
            >>> resp = data.restore_data('data_path')
        """
        if data_path is None:
            raise ValueError("Expect a date path")
        resp = self.__do_data('POST', data_path, operation='restore', end_slash=0)
        return RestoreDataResult(resp)
