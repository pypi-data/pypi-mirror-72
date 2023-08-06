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

from typing import List, Union

from email.message import Message
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import textwrap

from flask import current_app

str_or_list = Union[str, List[str]]

class EmailSender(object):
    def __init__(self,
                 sender: str_or_list=None,
                 recipient: str_or_list=None):
        self.sender = sender or current_app.config['STUDYGOV_EMAIL_FROM']
        recipient = recipient or current_app.config['STUDYGOV_EMAIL_TO']

        if isinstance(recipient, str):
            recipient = recipient.split(',')

        if not isinstance(recipient, list):
            recipient = list(recipient)

        self.recipient = recipient

    def send_email(self, subject: str, body: str, sender: str_or_list=None, recipient: str_or_list=None):
        mail_server = current_app.config['STUDYGOV_EMAIL_SERVER']
        prefix = current_app.config['STUDYGOV_EMAIL_PREFIX']

        if sender is None:
            sender = self.sender

        if recipient is None:
            recipient = self.recipient

        # The recipient always has to be a list
        if isinstance(recipient, str):
            recipient = [recipient]

        if not isinstance(recipient, list):
            recipient = list(recipient)

        message = MIMEMultipart('')
        message['Subject'] = '{prefix} {subject}'.format(prefix=prefix, subject=subject)
        message['To'] = ','.join(self.recipient)
        message['From'] = self.sender
        message.preamble = 'Automatically generated email of the {prefix}'.format(prefix=prefix)

        message_text = textwrap.dedent(body).strip()
        message.attach(MIMEText(message_text))

        # Make sure Message objects are turned into sendable strings
        if isinstance(message, Message):
            message = message.as_string()

        # Login and send
        print('[INFO] using mail server: {}'.format(mail_server))
        try:
            try:
                # First try SSL
                s = smtplib.SMTP_SSL(mail_server)
            except:
                # Fall back to normal
                s = smtplib.SMTP(mail_server)

            s.sendmail(sender, recipient, message)
            s.quit()
        except Exception as err:
            error_message = '[ERROR] Something went wrong when sending the email:\n{}'.format(err)
            print(error_message)
            return error_message

        return """Email send succesfully: 
FROM: {sender},
TO: {to},
SUBJECT: {subject},
BODY:\n{body}""".format(sender=sender, to=recipient, subject=subject, body=body)


def send_mail(experiment_url: str, 
              action_url: str, 
              subject: str, 
              body: str):
    """
    Send an email with SUBJECT and BODY.

    :param experiment_url: str, 
    :param action_url: str, 
    :param subject: str, 
    :param body: str):
    
    Substitution fields for SUBJECT and BODY are:

       - ``{experiment}``: experiment id
       - ``{experiment_url}``: full url for an experiment
       - ``{action_url}``: full url for an action.

    """

    email_sender = EmailSender()

    subject = subject.format(
        experiment=experiment_url.rsplit('/')[-1],
        experiment_url=experiment_url,
        action_url=action_url
    )

    body = body.format(
        experiment=experiment_url.rsplit('/')[-1],
        experiment_url=experiment_url,
        action_url=action_url
    )

    return email_sender.send_email(subject, body)
