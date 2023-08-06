# Copyright 2017 Biomedical Imaging Group Rotterdam, Departments of
# Medical Informatics and Radiology, Erasmus MC, Rotterdam, The Netherlands
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
import importlib
import yaml
import subprocess
import traceback

from flask import current_app


import requests
from urllib.parse import urlparse


def dispatch_callback(callback_data: str, action_url: str, config):
    """
    Dispatch the callback to the appropriate backend.
    """
    callback_method_name = config.get("STUDYGOV_CALLBACK_METHOD")
    callback_function = CALLBACK_BACKENDS.get(callback_method_name, 'local')
    current_app.logger.error(f'Using callback function {callback_function} with data {callback_data}  and action_url {action_url}')

    callback_function(callback_data, action_url, config)


def local_callback(callback_data: str, action_url: str, config=None):
    """
    This function dispatches a callback, at the moment it just creates a subprocess to handle the callback

    :param str callback_data: JSON string with description of the callback to use
    :param str action_url: the URL for the action that create the callback
    :param str experiment_url: the URL for the experiment linked to the callback
    :return:
    """
    # TODO: move this to a background watchdog thread that makes sure the program doesn't hang
    #       and can kill it when needed?
    current_app.logger.info('Local callback: {action_url}')
    callback_process = subprocess.Popen(['studygov-run-callback',
                                         '-c', callback_data,
                                         '-u', action_url])


def master_callback(callback_data: str, action_url: str):
    # current_app.logging.error('Master callback: {action_url}')
    callback_data = yaml.safe_load(callback_data)

    if callback_data is None:
        response = requests.put(action_url, json={
            "return_value": "No callback for state",
            "success": True,
            "end_time": datetime.datetime.now().isoformat()})
        print('Got response [{}] {}'.format(response.status_code, response.text))
        return

    function = callback_data.pop('function')
    callback_module = importlib.import_module('.{}'.format(function), 'studygovernor.callbacks')
    callback = getattr(callback_module, function)

    action_parsed_url = urlparse(action_url)

    # Get the experiment URL
    response = requests.get(action_url, headers={'Accept': 'application/json'})
    if response.status_code != 200:
        print('Got response [{}] {}'.format(response.status_code, response.text))
        return
    rel_experiment_uri = response.json()['experiment']
    experiment_url = f"{action_parsed_url.scheme}://{action_parsed_url.netloc}{rel_experiment_uri}"


    try:
        if callback is not None:
            result = callback(experiment_url, action_url, **callback_data)
        else:
            result = None
    except Exception as exception:
        print('Encountered exception in callback: {}'.format(exception))
        traceback.print_exc()

        return_value = "{}\n\n{}".format(exception, traceback.format_exc())
        success = False
    else:
        # Store results
        return_value = result
        success = True
    finally:
        end_time = datetime.datetime.now()

    if isinstance(return_value, str):
        return_value = return_value[:65536]  # Clip to textfield length for MySQL

    print('Setting callback result for action')
    response = requests.put(action_url, json={
                            "return_value": return_value,
                            "success": success,
                            "end_time": end_time.isoformat()})

    print('Got response [{}] {}'.format(response.status_code, response.text))

    return success


CALLBACK_BACKENDS = {
    'local': local_callback,
}

# Register the celery callback backend
from . import celery_backend
