# -*- coding: utf-8 -*-

import os

from flask import Flask
from flaskext.babel import Babel
from flask_mail import Mail


# Flaskup!
FLASKUP_TITLE = 'Flaskup!'
FLASKUP_UPLOAD_FOLDER = '/tmp/flaskup'
FLASKUP_MAX_DAYS = 30
FLASKUP_KEY_LENGTH = 6
FLASKUP_DELETE_KEY_LENGTH = 4
FLASKUP_ADMINS = []
FLASKUP_NOTIFY = []

# Flask
DEBUG = False
SECRET_KEY = 'change_asap'

# Babel
BABEL_DEFAULT_LOCALE = 'en'
BABEL_DEFAULT_TIMEZONE = 'UTC'

# Mail
DEFAULT_MAIL_SENDER = 'flaskup@example.com'
MAIL_SERVER = '127.0.0.1'
MAIL_PORT = 25

# Create our app
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKUP_CONFIG')


assert app.config['FLASKUP_MAX_DAYS'] > 0
assert app.config['FLASKUP_KEY_LENGTH'] >= 1 \
    and app.config['FLASKUP_KEY_LENGTH'] <= 32
assert app.config['FLASKUP_DELETE_KEY_LENGTH'] >= 1 \
    and app.config['FLASKUP_DELETE_KEY_LENGTH'] <= 32
assert os.access(app.config['FLASKUP_UPLOAD_FOLDER'], os.W_OK), \
    "No write access to '%s'" % app.config['FLASKUP_UPLOAD_FOLDER']


# Babel (i18n)
babel = Babel(app)

# Mail
mail = Mail(app)

# Load dependencies
import flaskup.views
import flaskup.filters
import flaskup.i18n
import flaskup.errorhandler
