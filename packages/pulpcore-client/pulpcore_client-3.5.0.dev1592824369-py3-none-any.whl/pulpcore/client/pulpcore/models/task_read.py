# coding: utf-8

"""
    Pulp 3 API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: v3
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from pulpcore.client.pulpcore.configuration import Configuration


class TaskRead(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'pulp_href': 'str',
        'pulp_created': 'datetime',
        'state': 'str',
        'name': 'str',
        'started_at': 'datetime',
        'finished_at': 'datetime',
        'error': 'dict(str, object)',
        'worker': 'str',
        'parent_task': 'str',
        'child_tasks': 'list[str]',
        'task_group': 'str',
        'progress_reports': 'list[ProgressReport]',
        'created_resources': 'list[str]',
        'reserved_resources_record': 'list[object]'
    }

    attribute_map = {
        'pulp_href': 'pulp_href',
        'pulp_created': 'pulp_created',
        'state': 'state',
        'name': 'name',
        'started_at': 'started_at',
        'finished_at': 'finished_at',
        'error': 'error',
        'worker': 'worker',
        'parent_task': 'parent_task',
        'child_tasks': 'child_tasks',
        'task_group': 'task_group',
        'progress_reports': 'progress_reports',
        'created_resources': 'created_resources',
        'reserved_resources_record': 'reserved_resources_record'
    }

    def __init__(self, pulp_href=None, pulp_created=None, state=None, name=None, started_at=None, finished_at=None, error=None, worker=None, parent_task=None, child_tasks=None, task_group=None, progress_reports=None, created_resources=None, reserved_resources_record=None, local_vars_configuration=None):  # noqa: E501
        """TaskRead - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._pulp_href = None
        self._pulp_created = None
        self._state = None
        self._name = None
        self._started_at = None
        self._finished_at = None
        self._error = None
        self._worker = None
        self._parent_task = None
        self._child_tasks = None
        self._task_group = None
        self._progress_reports = None
        self._created_resources = None
        self._reserved_resources_record = None
        self.discriminator = None

        if pulp_href is not None:
            self.pulp_href = pulp_href
        if pulp_created is not None:
            self.pulp_created = pulp_created
        if state is not None:
            self.state = state
        self.name = name
        if started_at is not None:
            self.started_at = started_at
        if finished_at is not None:
            self.finished_at = finished_at
        if error is not None:
            self.error = error
        if worker is not None:
            self.worker = worker
        if parent_task is not None:
            self.parent_task = parent_task
        if child_tasks is not None:
            self.child_tasks = child_tasks
        if task_group is not None:
            self.task_group = task_group
        if progress_reports is not None:
            self.progress_reports = progress_reports
        if created_resources is not None:
            self.created_resources = created_resources
        if reserved_resources_record is not None:
            self.reserved_resources_record = reserved_resources_record

    @property
    def pulp_href(self):
        """Gets the pulp_href of this TaskRead.  # noqa: E501


        :return: The pulp_href of this TaskRead.  # noqa: E501
        :rtype: str
        """
        return self._pulp_href

    @pulp_href.setter
    def pulp_href(self, pulp_href):
        """Sets the pulp_href of this TaskRead.


        :param pulp_href: The pulp_href of this TaskRead.  # noqa: E501
        :type: str
        """

        self._pulp_href = pulp_href

    @property
    def pulp_created(self):
        """Gets the pulp_created of this TaskRead.  # noqa: E501

        Timestamp of creation.  # noqa: E501

        :return: The pulp_created of this TaskRead.  # noqa: E501
        :rtype: datetime
        """
        return self._pulp_created

    @pulp_created.setter
    def pulp_created(self, pulp_created):
        """Sets the pulp_created of this TaskRead.

        Timestamp of creation.  # noqa: E501

        :param pulp_created: The pulp_created of this TaskRead.  # noqa: E501
        :type: datetime
        """

        self._pulp_created = pulp_created

    @property
    def state(self):
        """Gets the state of this TaskRead.  # noqa: E501

        The current state of the task. The possible values include: 'waiting', 'skipped', 'running', 'completed', 'failed' and 'canceled'.  # noqa: E501

        :return: The state of this TaskRead.  # noqa: E501
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state):
        """Sets the state of this TaskRead.

        The current state of the task. The possible values include: 'waiting', 'skipped', 'running', 'completed', 'failed' and 'canceled'.  # noqa: E501

        :param state: The state of this TaskRead.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                state is not None and len(state) < 1):
            raise ValueError("Invalid value for `state`, length must be greater than or equal to `1`")  # noqa: E501

        self._state = state

    @property
    def name(self):
        """Gets the name of this TaskRead.  # noqa: E501

        The name of task.  # noqa: E501

        :return: The name of this TaskRead.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this TaskRead.

        The name of task.  # noqa: E501

        :param name: The name of this TaskRead.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                name is not None and len(name) < 1):
            raise ValueError("Invalid value for `name`, length must be greater than or equal to `1`")  # noqa: E501

        self._name = name

    @property
    def started_at(self):
        """Gets the started_at of this TaskRead.  # noqa: E501

        Timestamp of the when this task started execution.  # noqa: E501

        :return: The started_at of this TaskRead.  # noqa: E501
        :rtype: datetime
        """
        return self._started_at

    @started_at.setter
    def started_at(self, started_at):
        """Sets the started_at of this TaskRead.

        Timestamp of the when this task started execution.  # noqa: E501

        :param started_at: The started_at of this TaskRead.  # noqa: E501
        :type: datetime
        """

        self._started_at = started_at

    @property
    def finished_at(self):
        """Gets the finished_at of this TaskRead.  # noqa: E501

        Timestamp of the when this task stopped execution.  # noqa: E501

        :return: The finished_at of this TaskRead.  # noqa: E501
        :rtype: datetime
        """
        return self._finished_at

    @finished_at.setter
    def finished_at(self, finished_at):
        """Sets the finished_at of this TaskRead.

        Timestamp of the when this task stopped execution.  # noqa: E501

        :param finished_at: The finished_at of this TaskRead.  # noqa: E501
        :type: datetime
        """

        self._finished_at = finished_at

    @property
    def error(self):
        """Gets the error of this TaskRead.  # noqa: E501

        A JSON Object of a fatal error encountered during the execution of this task.  # noqa: E501

        :return: The error of this TaskRead.  # noqa: E501
        :rtype: dict(str, object)
        """
        return self._error

    @error.setter
    def error(self, error):
        """Sets the error of this TaskRead.

        A JSON Object of a fatal error encountered during the execution of this task.  # noqa: E501

        :param error: The error of this TaskRead.  # noqa: E501
        :type: dict(str, object)
        """

        self._error = error

    @property
    def worker(self):
        """Gets the worker of this TaskRead.  # noqa: E501

        The worker associated with this task. This field is empty if a worker is not yet assigned.  # noqa: E501

        :return: The worker of this TaskRead.  # noqa: E501
        :rtype: str
        """
        return self._worker

    @worker.setter
    def worker(self, worker):
        """Sets the worker of this TaskRead.

        The worker associated with this task. This field is empty if a worker is not yet assigned.  # noqa: E501

        :param worker: The worker of this TaskRead.  # noqa: E501
        :type: str
        """

        self._worker = worker

    @property
    def parent_task(self):
        """Gets the parent_task of this TaskRead.  # noqa: E501

        The parent task that spawned this task.  # noqa: E501

        :return: The parent_task of this TaskRead.  # noqa: E501
        :rtype: str
        """
        return self._parent_task

    @parent_task.setter
    def parent_task(self, parent_task):
        """Sets the parent_task of this TaskRead.

        The parent task that spawned this task.  # noqa: E501

        :param parent_task: The parent_task of this TaskRead.  # noqa: E501
        :type: str
        """

        self._parent_task = parent_task

    @property
    def child_tasks(self):
        """Gets the child_tasks of this TaskRead.  # noqa: E501

        Any tasks spawned by this task.  # noqa: E501

        :return: The child_tasks of this TaskRead.  # noqa: E501
        :rtype: list[str]
        """
        return self._child_tasks

    @child_tasks.setter
    def child_tasks(self, child_tasks):
        """Sets the child_tasks of this TaskRead.

        Any tasks spawned by this task.  # noqa: E501

        :param child_tasks: The child_tasks of this TaskRead.  # noqa: E501
        :type: list[str]
        """

        self._child_tasks = child_tasks

    @property
    def task_group(self):
        """Gets the task_group of this TaskRead.  # noqa: E501

        The task group that this task is a member of.  # noqa: E501

        :return: The task_group of this TaskRead.  # noqa: E501
        :rtype: str
        """
        return self._task_group

    @task_group.setter
    def task_group(self, task_group):
        """Sets the task_group of this TaskRead.

        The task group that this task is a member of.  # noqa: E501

        :param task_group: The task_group of this TaskRead.  # noqa: E501
        :type: str
        """

        self._task_group = task_group

    @property
    def progress_reports(self):
        """Gets the progress_reports of this TaskRead.  # noqa: E501


        :return: The progress_reports of this TaskRead.  # noqa: E501
        :rtype: list[ProgressReport]
        """
        return self._progress_reports

    @progress_reports.setter
    def progress_reports(self, progress_reports):
        """Sets the progress_reports of this TaskRead.


        :param progress_reports: The progress_reports of this TaskRead.  # noqa: E501
        :type: list[ProgressReport]
        """

        self._progress_reports = progress_reports

    @property
    def created_resources(self):
        """Gets the created_resources of this TaskRead.  # noqa: E501

        Resources created by this task.  # noqa: E501

        :return: The created_resources of this TaskRead.  # noqa: E501
        :rtype: list[str]
        """
        return self._created_resources

    @created_resources.setter
    def created_resources(self, created_resources):
        """Sets the created_resources of this TaskRead.

        Resources created by this task.  # noqa: E501

        :param created_resources: The created_resources of this TaskRead.  # noqa: E501
        :type: list[str]
        """

        self._created_resources = created_resources

    @property
    def reserved_resources_record(self):
        """Gets the reserved_resources_record of this TaskRead.  # noqa: E501


        :return: The reserved_resources_record of this TaskRead.  # noqa: E501
        :rtype: list[object]
        """
        return self._reserved_resources_record

    @reserved_resources_record.setter
    def reserved_resources_record(self, reserved_resources_record):
        """Sets the reserved_resources_record of this TaskRead.


        :param reserved_resources_record: The reserved_resources_record of this TaskRead.  # noqa: E501
        :type: list[object]
        """

        self._reserved_resources_record = reserved_resources_record

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, TaskRead):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, TaskRead):
            return True

        return self.to_dict() != other.to_dict()
