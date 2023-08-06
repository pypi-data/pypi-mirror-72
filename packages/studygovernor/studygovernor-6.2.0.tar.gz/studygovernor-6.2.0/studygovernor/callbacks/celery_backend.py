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


from flask import current_app
from studygovernor.callbacks import CALLBACK_BACKENDS, master_callback
import os

try:
    from celery.signals import worker_process_init
    from celery import Celery, signals
    CELERY_IMPORTED = True
except ImportError:
    CELERY_IMPORTED = False

# If raven is used, try to setup raven to catch celery stuff
try:
    from raven.contrib.celery import register_signal, register_logger_signal
    from studygovernor import sentry
    client = sentry.client

    # register a custom filter to filter out duplicate logs
    register_logger_signal(client)

    # The register_signal function can also take an optional argument
    # `ignore_expected` which causes exception classes specified in Task.throws
    # to be ignored
    register_signal(client, ignore_expected=True)
    
except ImportError:
    pass


def task_callback(celery_self, callback_data: str, action_url: str):
    try:
        master_callback(callback_data, action_url)
    except Exception as exc:
        celery_self.retry(exc=exc)
        

def celery_callback(callback_data: str, action_url: str, config=None):
    if not CELERY_IMPORTED:
        raise ImportError("Cannot use celery callback, celery python package appears not to be installed!")
    
    celery = Celery('studygovernor_callbacks',
                    backend=config['STUDYGOV_CELERY_BACKEND'],
                    broker=config['STUDYGOV_CELERY_BROKER'])

    current_app.logger.error('Creating task')
    # Directly call the decorator runtime instead of during import time
    #task = celery.task(bind=True, default_retry_delay=1)(task_callback)
    task = celery.task(bind=True)(task_callback)
    current_app.logger.error(f'Created: {task}')

    current_app.logger.error(f'delay celery callback: {action_url}')
    result = task.delay(callback_data, action_url)
    current_app.logger.error(f'Delayed task status: {result.status}')


CALLBACK_BACKENDS['celery'] = celery_callback
