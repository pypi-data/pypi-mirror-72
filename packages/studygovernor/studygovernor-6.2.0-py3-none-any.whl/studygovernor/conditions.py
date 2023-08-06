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

import importlib
import json
import traceback
from . import exceptions


def master_condition(experiment, data, condition_id):
    data = json.loads(data)

    function = data['function'].rsplit('.', 1)
    try:
        function = getattr(importlib.import_module(function[0]), function[1])
    except (ImportError, AttributeError):
        raise exceptions.UnknownConditionFunction(condition=condition_id,
                                                  module=function[0],
                                                  function=function[1])

    args = None
    kwargs = None

    try:
        args = data.get('args', [])
        kwargs = data.get('kwargs', {})
        result = function(experiment, *args, **kwargs)
    except:
        stacktrace = traceback.format_exc()
        raise exceptions.ConditionFunctionCallFailedError(condition=condition_id,
                                                          function='{}.{}'.format(function.__module__,
                                                                                  function.__name__),
                                                          args=args,
                                                          kwargs=kwargs,
                                                          stacktrace=stacktrace)

    if not isinstance(result, bool):
        raise exceptions.ConditionFunctionReturnValueError(condition=condition_id,
                                                           function='{}.{}'.format(function.__module__,
                                                                                   function.__name__),
                                                           args=args,
                                                           kwargs=kwargs,
                                                           return_value=result)

    return result


def id_equals(experiment, wanted_id):
    exp_id = experiment.id
    print('Comparing experiment id {} ({}) to wanted id {} ({})'.format(exp_id,
                                                                        type(exp_id).__name__,
                                                                        wanted_id,
                                                                        type(wanted_id).__name__))

    return exp_id == wanted_id


condition_example = \
    """
    {
      "function": "studygovernor.conditions.id_equals",
      "args": [2]
    }
    """
