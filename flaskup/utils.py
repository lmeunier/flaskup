# -*- coding: utf-8 -*-

from flask.ext.mail import Message
from flaskup import mail


def send_mail(subject, body, recipients):
    # remove new lines from subject
    subject = ' '.join(subject.strip().splitlines())

    msg = Message(subject, recipients=recipients)
    msg.body = body

    try:
        mail.send(msg)
    except:
        # this is likely to be a bad recipient address
        # ... or a failure in the MTA
        # in any case, we don't want to bother the user with these errors
        # so we fail silently
        pass
