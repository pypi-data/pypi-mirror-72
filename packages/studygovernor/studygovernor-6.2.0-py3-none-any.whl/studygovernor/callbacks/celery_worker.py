import os
from flask import current_app
from celery import Celery

from .celery_backend import task_callback
from .. import create_app

app = create_app()
app.app_context().push()

celery = Celery('studygovernor_callbacks',
                backend=current_app.config['STUDYGOV_CELERY_BACKEND'],
                broker=current_app.config['STUDYGOV_CELERY_BROKER'])

task = celery.task(bind=True)(task_callback)
