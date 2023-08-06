import docker

# "image": "bigr/fastr:develop",
# "volumes": {
#     "/Users/adriaan/Projects/2018_HACKATHON/pipelines/iris": {"bind": "/Users/adriaan/Projects/2018_HACKATHON/pipelines/iris", "mode": "rw"},
#     "/Users/adriaan/Projects/2018_HACKATHON/pipelines/fastr-tmp": {"bind": "/Users/adriaan/Projects/2018_HACKATHON/pipelines/fastr-tmp", "mode": "rw"},
#     "/Users/adriaan/Projects/2018_HACKATHON/pipelines/fastr-out": {"bind": "/Users/adriaan/Projects/2018_HACKATHON/pipelines/fastr-out", "mode": "rw"}
# },
# "cmd": ["python", "qa-script.py", "--experiment"],
# "arguments": {
#     "--xnat": "http://xnat.bigr.infra",
#     "--project" : "sandbox",
#     "--pipeline_succes" : "/api/v1/states/create_inspection_task",
#     "--pipeline_failed" : "/api/v1/states/dcm2niix_failed"
# }


def docker_run(experiment_url: str,
               action_url: str,
               image: str,
               progress_state=None,
               args=None,
               volumes=None,
               environment=None,
               cmd=None,
               xnat_external_system_name: str='XNAT'):
    """
    Run docker container task

    :param experiment_url: str
    :param action_url: str
    :param image: str
    :param progress_state: None
    :param args: None
    :param volumes: None
    :param environment: None
    :param cmd: None
    :param xnat_external_system_name: name of the external xnat [XNAT]

    The items in args that contain certain VARS will be replaced. Accepted VARS:

    - $EXPERIMENT - will be substituted with the experiment URL.
    - $XNAT - will be substituted with the xnat URL.

    Example:

    .. code-block:: JSON

       {
         "function": "create_task",
         "image": "bigr/fastr:develop",
         "volumes": {
             "pipelines/atlas": {"bind": "pipelines/atlas", "mode": "rw"},
             "pipelines/params": {"bind": "pipelines/params", "mode": "rw"}
         },
         "cmd": ["python", "qa-script.py"],
         "args": {
             "--experiment": "$EXPERIMENT",
             "--xnat": "$XNAT",
             "--project" : "sandbox",
             "--pipeline_succes" : "/api/v1/states/create_inspection_task",
             "--pipeline_failed" : "/api/v1/states/QA_failed"
         }
       }

    """

    # Get XNAT address from database
    xnat = ExternalSystem.query.filter(ExternalSystem.system_name == xnat_external_system_name).one()
    xnat_uri = xnat.url.rstrip('/')
    args = [x.replace("$XNAT", xnat_uri) for x in args]

    # Get XNAT address from Database
    experiment = str(experiment)
    args = [x.replace("$EXPERIMENT", experiment) for x in args]

    command = [str(x) for x in cmd] + [str(experiment_url)] + [str(x) for k, v in arguments.items() for x in [k, v]]
    print('[CALLBACK docker-run] experiment:{}'.format(experiment_url))
    print('[CALLBACK docker-run] action_url:{}'.format(action_url))
    print('[CALLBACK docker-run] image:{}'.format(image))
    print('[CALLBACK docker-run] cmd:{}'.format(command))
    print('[CALLBACK docker-run] progress_state:{}'.format(progress_state))

    #client = docker.APIClient(base_url='unix://var/run/docker.sock')
    client = docker.from_env()
    output = client.containers.run(image, command, environment=environment, volumes=volumes)
    print('[CALLBACK docker-run] outout: {}'.format(output))
