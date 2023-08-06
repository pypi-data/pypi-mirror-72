Study Governor is a controller for data in large population imaging studies.

Documentation
=============

The Study Governor is documented at https://idsp-study-governor.readthedocs.io/


Installation and operation instructions
=======================================

 1. Install `mysql` and `libmysqlclient-dev` (e.g. `sudo apt-get install mysql-server libmysqlclient-dev`)
 2. Run `python setup.py install` (or `python setup.py develop` inside a virtualenv if developing)
 3. Create the database in the following way:

``
# Go the mysql command line (add the -p if you have set a root password).
$ sudo mysql (-p)

# Create user
mysql> CREATE USER 'studygovernor'@'localhost' IDENTIFIED BY 'blaat123';

# Create database
mysql> CREATE DATABASE studygovernor;

# Grant all permissions of the database to the user.
mysql> GRANT ALL ON studygovernor.* TO 'studygovernor'@'localhost';
``

 4. Run `studygov-db-init` to initialize the database.


Adding some stuff via REST
==========================

>>> sub = {'label': 'sub_001', 'date_of_birth': '2000-12-25'}
>>> requests.post('http://localhost:5000/api/v1/subjects', json=sub)
>>> exp = {'label': 'exp_001', 'subject': '/api/v1/subjects/1', 'scandate': datetime.datetime.now().isoformat()}
>>> requests.post('http://localhost:5000/api/v1/experiments', json=exp)
>>> requests.get('http://localhost:5000/api/v1/experiments/1/state')
>>> requests.put('http://localhost:5000/api/v1/experiments/1/state', json={'state': '/api/v1/states/3'})
