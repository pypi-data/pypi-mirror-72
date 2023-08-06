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

from flask import url_for
from flask_restplus import fields


class MappingField(fields.Raw):
    def __init__(self, **kwargs):
        super(MappingField, self).__init__(**kwargs)

    def format(self, value):
        return {str(k): str(v) for k, v in value.items()}


class ObjectUrl(fields.Raw):
    __schema_type__ = "string"

    def __init__(self, object_class, api_prefix=None, **kwargs):
        super(ObjectUrl, self).__init__(**kwargs)
        self._object_class = object_class
        self.api_prefix = api_prefix

    def format(self, value):
        if self.api_prefix:
            result = url_for('{}.{}'.format(self.api_prefix,
                                            self._object_class), id=value)
        else:
            result = url_for(self._object_class, id=value)
        return result


class SubUrl(fields.Raw):
    __schema_type__ = "string"

    def __init__(self, object_class, subfield, **kwargs):
        super(SubUrl, self).__init__(**kwargs)
        self._object_class = object_class
        self._subfield = subfield

    def format(self, value):
        url = url_for(self._object_class, id=value)

        return '{}/{}'.format(url, self._subfield)
