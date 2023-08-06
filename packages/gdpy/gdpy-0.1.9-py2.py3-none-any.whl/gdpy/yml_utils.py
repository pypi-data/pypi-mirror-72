# -*- coding:utf-8 -*-
import collections
import sys

import yaml

from .utils import json_loader

is_py2 = (sys.version_info[0] == 2)
is_py3 = (sys.version_info[0] == 3)

default_encoding = "utf-8"

if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    getattr(sys, 'setdefaultencoding', lambda *args: None)("utf-8")


def yaml_loader(file_name):
    with open(file_name, 'r') as f:
        return yaml.load(f.read(), yaml.SafeLoader)


def yaml_dumper(data):
    return yaml.safe_dump(data, default_flow_style=False, encoding=('utf-8'), allow_unicode=True)


if is_py2:
    def convert(data):
        if isinstance(data, basestring):
            return str(data).encode('utf-8')
        elif isinstance(data, collections.Mapping):
            return dict(map(convert, data.iteritems()))
        elif isinstance(data, collections.Iterable):
            return type(data)(map(convert, data))
        else:
            return data
elif is_py3:
    def convert(data):
        if isinstance(data, (str, bytes)):
            return data
        elif isinstance(data, collections.Mapping):
            return dict(map(convert, data.items()))
        elif isinstance(data, collections.Iterable):
            return type(data)(map(convert, data))
        else:
            return data


def parse_list_tasks(result, body):
    body = json_loader(body)
    if isinstance(body, list):
        # TODO this is the patch for the beta API (WDL)
        body = {
            "task_list": body,
            "count": len(body),
            "total": len(body)
        }
    result.task_list = convert(body).get('task_list')
    result.count = body.get('count', 0)
    result.total = body.get('total', 0)
    return result


def parse_get_jobs(result, body):
    body = json_loader(body)
    if isinstance(body, list):
        # TODO this is the patch for the beta API (WDL)
        body = {
            "jobs": body,
        }
    result.jobs = convert(body).get('jobs')
    result.count = len(result.jobs)
    return result


def parse_list_workflows(result, body, workflow_type='gwl'):
    body = json_loader(body)
    if workflow_type == 'gwl':
        result.workflows = convert(body).get('items')
        result.count = len(result.workflows)
    elif workflow_type == 'wdl':
        result.workflows = convert(body)
    else:
        raise NotImplementedError("Unsupported workflow type '{}'".format(workflow_type))
    return result


def parse_list_tools(result, body):
    body = json_loader(body)
    result.tools = convert(body).get('items')
    result.count = len(result.tools)
    return result


def parse_get_tool_parameters(result, body):
    body = json_loader(body)
    result.parameters = convert(body).get('parameter')
    return result
