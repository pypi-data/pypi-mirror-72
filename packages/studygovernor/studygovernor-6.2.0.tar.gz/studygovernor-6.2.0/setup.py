# Copyright 2017-2020 Biomedical Imaging Group Rotterdam, Departments of
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

import os
from setuptools import setup

# Parse requirements file
with open('requirements.txt', 'r') as fh:
    _requires = fh.read().splitlines()

with open('test_requirements.txt', 'r') as fh:
    _tests_require = fh.read().splitlines()

entry_points = {
    "console_scripts": [
        "studygov-db-init = studygovernor.__main__:db_init",
        "studygov-db-clean = studygovernor.__main__:db_clean",
        "studygov-workflow-init = studygovernor.__main__:workflow_init",
        "studygov-workflow-visualize = studygovernor.__main__:visualize_workflow",
        "studygov-test-data = studygovernor.__main__:test_data",
        "studygov-create-subject = studygovernor.__main__:create_subject",
        "studygov-create-experiment = studygovernor.__main__:create_experiment",
        "studygov-manager = studygovernor.__main__:flask_manager",
        "studygov-run-callback = studygovernor.__main__:run_callback",
        "studygov-parse-pontiac = studygovernor.__main__:parse_pontiac_dump",
        "studygov-config = studygovernor.__main__:config_from_file",
    ],
}

VERSION = '6.2.0'
# When building something else than a release (tag) append the job id to the version.
if os.environ.get('CI_COMMIT_TAG'):
    pass
elif os.environ.get('CI_JOB_ID'):
    VERSION += f".{os.environ['CI_JOB_ID']}"

setup(
    name='studygovernor',
    version=VERSION,
    author='H.C. Achterberg, M. Koek, A. Versteeg, M. Birhanu',
    author_email='h.achterberg@erasmusmc.nl, m.koek@erasmusmc.nl, a.versteeg@erasmusmc.nl, m.birhanu@erasmusmc.nl',
    packages=[
        'studygovernor',
        'studygovernor.api',
        'studygovernor.auth',
        'studygovernor.callbacks',
        'studygovernor.services',
        'studygovernor.services.pidb',
        'studygovernor.util',
    ],
    package_data = {'studygovernor': ['templates/*', 'templates/**/*', 'static/*', 'static/**/*']},
    url='https://gitlab.com/radiology/infrastructure/study-governor',
    license='Apache 2.0',
    description='Study Governor is a controller for data in large population imaging studies.',
    long_description=open('README.rst').read(),
    long_description_content_type='text/x-rst',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Healthcare Industry',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Education',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: System :: Logging',
        'Topic :: Utilities',
    ],
    setup_requires=["pytest-runner"],
    install_requires=_requires,
    entry_points=entry_points,
    tests_require=_tests_require,
    scripts=['bin/fastr_python_launcher']
)
