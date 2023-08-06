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

import json
from flask_restplus import marshal, fields
from studygovernor.fields import ObjectUrl

from werkzeug.exceptions import HTTPException

class StudyGovernorError(Exception):
    """
    Base class for exceptions in the study governor codebase
    """
    _fields = {}

    @property
    def fields(self):
        return self._fields

    def marshal(self, api_prefix):
        fields = dict(self._fields)
        for field in fields.values():
            if isinstance(field, ObjectUrl):
                field.api_prefix = api_prefix

        return marshal(self, fields)

class StudyGovernorHTTPError(StudyGovernorError, HTTPException):
    """
    All exceptions that should lead to an HTTP error response
    """
    code = 500

    def __init__(self, description, response=None):
        super().__init__(description)
        self._description = description

    def __str__(self):
        return str(self._description)

    @property
    def description(self):
        return str(self)


class CouldNotFindResourceError(StudyGovernorHTTPError):
    """
    Could not find a resource
    """
    code = 404

    def __init__(self, id_, type_, message=None):
        super().__init__(message)
        self.id = id_
        self.type =type_
        self.msg = message

    def __str__(self):
        if self.msg is not None:
            return self.msg.format(id=self.id, type_=self.type)
        else:
            return f"Could not find {self.type.__name__} with identifier {self.id!r}"


class StateChangeError(StudyGovernorError):
    """
    Exceptions encountered during a state change
    """


class NoValidTransitionError(StateChangeError):
    _fields = {
        'errorclass': fields.String,
        'sourcestate': ObjectUrl('state', attribute='sourcestate'),
        'targetstate': ObjectUrl('state', attribute='targetstate'),
        'message': fields.String,
    }

    def __init__(self, sourcestate, targetstate):
        self.errorclass = type(self).__name__
        self.sourcestate = sourcestate.id
        self.targetstate = targetstate.id
        self.message = 'Could not find a valid transition for requested' \
                       ' state change (from {} [{}] to {} [{}])'.format(sourcestate.label,
                                                                        sourcestate.id,
                                                                        targetstate.label,
                                                                        targetstate.id)


class StateNotFoundError(StateChangeError):
    _fields = {
        'errorclass': fields.String,
        'requested_state': fields.String,
        'message': fields.String,
    }

    def __init__(self, requested_state):
        self.errorclass = type(self).__name__
        self.requested_state = requested_state
        self.message = 'Could not found requested state "{}"'.format(requested_state)


class ConditionNotMetError(StateChangeError):
    _fields = {
        'errorclass': fields.String,
        'transition': ObjectUrl('transition'),
        'condition': ObjectUrl('condition'),
        'condition_rule': fields.Raw,
        'message': fields.String,
    }

    def __init__(self, experiment, transition, condition):
        self.errorclass = type(self).__name__
        self.transition = transition.id
        self.condition = condition.id
        self.condition_rule = json.loads(condition.rule)
        self.experiment = experiment.id
        self.message ='A condition ({}) for a transition ({}) was not met!'.format(transition.id,
                                                                                   condition.id)


class UnknownConditionFunction(StateChangeError):
    _fields = {
        'errorclass': fields.String,
        'condition': ObjectUrl('condition'),
        'module': fields.String,
        'function': fields.String,
        'message': fields.String,
    }

    def __init__(self, condition, module, function):
        self.errorclass = type(self).__name__
        self.condition = condition
        self.module = module
        self.function = function
        self.message = ("the function '{}' in module '{}' for validating"
                        " condition {} cannot be found!").format(function,
                                                                 module,
                                                                 condition)


class ConditionFunctionCallFailedError(StateChangeError):
    _fields = {
        'errorclass': fields.String,
        'condition': ObjectUrl('condition'),
        'function': fields.String,
        'arguments': fields.Raw,
        'keyword_arguments': fields.Raw,
        'stacktrace': fields.String,
        'message': fields.String,
    }

    def __init__(self, condition, function, args, kwargs, stacktrace):
        self.errorclass = type(self).__name__
        self.condition = condition
        self.arguments = args
        self.keyword_arguments = kwargs
        self.stacktrace = stacktrace
        all_arguments = ', '.join([str(x) for x in args] + ['{}={}'.format(k, v) for k, v in kwargs.items()])
        self.message = "Calling conditional function {}({}) resulted in exceptions!".format(function, all_arguments)


class ConditionFunctionReturnValueError(ConditionFunctionCallFailedError):
    _fields = {
        'errorclass': fields.String,
        'condition': ObjectUrl('condition'),
        'function': fields.String,
        'arguments': fields.Raw,
        'keyword_arguments': fields.Raw,
        'return_value_type': fields.String,
        'message': fields.String,
    }

    def __init__(self, condition, function, args, kwargs, return_value):
        super(ConditionFunctionReturnValueError, self).__init__(condition=condition,
                                                                function=function,
                                                                args=args,
                                                                kwargs=kwargs,
                                                                stacktrace='')

        self.return_value_type = type(return_value).__name__
        self.message = "Invalid return value for conditional function '{}' (bool expected, found {})".format(function,
                                                                                                             type(return_value).__name__)



class StudyGovernorClientError(StudyGovernorError):
    """
    Error class for all client-side errors
    """


class RESTResponseError(StudyGovernorClientError):
    """
    The REST response is not what was expected
    """


class StudyGovernorSSLError(StudyGovernorClientError):
    """
    There was a problem creating an SSL connection
    """
