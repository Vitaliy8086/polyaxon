# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os
import shutil

from django.conf import settings

from libs.paths import delete_path, create_path


def get_experiment_outputs_path(experiment_name):
    values = experiment_name.split('.')
    if len(values) == 3:
        values.insert(2, 'independents')
    return os.path.join(settings.OUTPUTS_ROOT, '/'.join(values))


def get_experiment_logs_path(experiment_name):
    values = experiment_name.split('.')
    if len(values) == 3:
        values.insert(2, 'independents')
    return os.path.join(settings.LOGS_ROOT, '/'.join(values))


def delete_experiment_logs(experiment_group_name):
    path = get_experiment_logs_path(experiment_group_name)
    delete_path(path)


def delete_experiment_outputs(experiment_group_name):
    path = get_experiment_outputs_path(experiment_group_name)
    delete_path(path)


def create_experiment_path(experiment_name, path):
    values = experiment_name.split('.')
    if len(values) == 3:
        values.insert(2, 'independents')

    for value in values[:-1]:
        path = os.path.join(path, value)
        if not os.path.isdir(path):
            create_path(path)

    return path


def create_experiment_logs_path(experiment_name):
    values = experiment_name.split('.')
    path = create_experiment_path(experiment_name, settings.LOGS_ROOT)

    # Create file with permissions
    path = os.path.join(path, values[-1])
    open(path, 'w+')
    os.chmod(path, 0o777)
    return path


def create_experiment_outputs_path(experiment_name):
    values = experiment_name.split('.')
    path = create_experiment_path(experiment_name, settings.OUTPUTS_ROOT)
    path = os.path.join(path, values[-1])
    if not os.path.isdir(path):
        create_path(path)
    return path


def copy_experiment_outputs(experiment_name_from, experiment_name_to):
    path_from = get_experiment_outputs_path(experiment_name_from)
    path_to = get_experiment_outputs_path(experiment_name_to)
    shutil.copytree(path_from, path_to)
