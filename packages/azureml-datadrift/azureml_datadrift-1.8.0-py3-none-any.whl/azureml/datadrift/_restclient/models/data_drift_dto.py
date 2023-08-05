# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator 1.0.0.0
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class DataDriftDto(Model):
    """DataDriftDto.

    :param frequency:
    :type frequency: str
    :param schedule_start_time:
    :type schedule_start_time: datetime
    :param schedule_id:
    :type schedule_id: str
    :param interval:
    :type interval: int
    :param state: Possible values include: 'Disabled', 'Enabled', 'Deleted',
     'Disabling', 'Enabling', 'Deleting', 'Failed', 'DeleteFailed',
     'EnableFailed', 'DisableFailed'
    :type state: str or ~_restclient.models.enum
    :param alert_configuration:
    :type alert_configuration: ~_restclient.models.AlertConfiguration
    :param alert_id:
    :type alert_id: str
    :param latest_run_time:
    :type latest_run_time: datetime
    :param latest_run_state: Possible values include: 'Failed', 'Canceled',
     'UserError', 'Finished'
    :type latest_run_state: str or ~_restclient.models.enum
    :param azure_monitor_error:
    :type azure_monitor_error: str
    :param id:
    :type id: str
    :param name:
    :type name: str
    :param type: Possible values include: 'ModelBased', 'DatasetBased'
    :type type: str or ~_restclient.models.enum
    :param model_name:
    :type model_name: str
    :param model_version:
    :type model_version: int
    :param base_dataset_id:
    :type base_dataset_id: str
    :param target_dataset_id:
    :type target_dataset_id: str
    :param services:
    :type services: list[str]
    :param compute_target_name:
    :type compute_target_name: str
    :param features:
    :type features: list[str]
    :param drift_threshold:
    :type drift_threshold: float
    :param job_latency:
    :type job_latency: int
    :param created_time:
    :type created_time: datetime
    :param experiment_name:
    :type experiment_name: str
    """

    _attribute_map = {
        'frequency': {'key': 'frequency', 'type': 'str'},
        'schedule_start_time': {'key': 'scheduleStartTime', 'type': 'iso-8601'},
        'schedule_id': {'key': 'scheduleId', 'type': 'str'},
        'interval': {'key': 'interval', 'type': 'int'},
        'state': {'key': 'state', 'type': 'str'},
        'alert_configuration': {'key': 'alertConfiguration', 'type': 'AlertConfiguration'},
        'alert_id': {'key': 'alertId', 'type': 'str'},
        'latest_run_time': {'key': 'latestRunTime', 'type': 'iso-8601'},
        'latest_run_state': {'key': 'latestRunState', 'type': 'str'},
        'azure_monitor_error': {'key': 'azureMonitorError', 'type': 'str'},
        'id': {'key': 'id', 'type': 'str'},
        'name': {'key': 'name', 'type': 'str'},
        'type': {'key': 'type', 'type': 'str'},
        'model_name': {'key': 'modelName', 'type': 'str'},
        'model_version': {'key': 'modelVersion', 'type': 'int'},
        'base_dataset_id': {'key': 'baseDatasetId', 'type': 'str'},
        'target_dataset_id': {'key': 'targetDatasetId', 'type': 'str'},
        'services': {'key': 'services', 'type': '[str]'},
        'compute_target_name': {'key': 'computeTargetName', 'type': 'str'},
        'features': {'key': 'features', 'type': '[str]'},
        'drift_threshold': {'key': 'driftThreshold', 'type': 'float'},
        'job_latency': {'key': 'jobLatency', 'type': 'int'},
        'created_time': {'key': 'createdTime', 'type': 'iso-8601'},
        'experiment_name': {'key': 'experimentName', 'type': 'str'},
    }

    def __init__(self, **kwargs):
        super(DataDriftDto, self).__init__(**kwargs)
        self.frequency = kwargs.get('frequency', None)
        self.schedule_start_time = kwargs.get('schedule_start_time', None)
        self.schedule_id = kwargs.get('schedule_id', None)
        self.interval = kwargs.get('interval', None)
        self.state = kwargs.get('state', None)
        self.alert_configuration = kwargs.get('alert_configuration', None)
        self.alert_id = kwargs.get('alert_id', None)
        self.latest_run_time = kwargs.get('latest_run_time', None)
        self.latest_run_state = kwargs.get('latest_run_state', None)
        self.azure_monitor_error = kwargs.get('azure_monitor_error', None)
        self.id = kwargs.get('id', None)
        self.name = kwargs.get('name', None)
        self.type = kwargs.get('type', None)
        self.model_name = kwargs.get('model_name', None)
        self.model_version = kwargs.get('model_version', None)
        self.base_dataset_id = kwargs.get('base_dataset_id', None)
        self.target_dataset_id = kwargs.get('target_dataset_id', None)
        self.services = kwargs.get('services', None)
        self.compute_target_name = kwargs.get('compute_target_name', None)
        self.features = kwargs.get('features', None)
        self.drift_threshold = kwargs.get('drift_threshold', None)
        self.job_latency = kwargs.get('job_latency', None)
        self.created_time = kwargs.get('created_time', None)
        self.experiment_name = kwargs.get('experiment_name', None)
