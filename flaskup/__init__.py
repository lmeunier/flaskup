# -*- coding: utf-8 -*-

from flask import Flask
from flaskext.babel import Babel
from flaskext.mail import Mail


# Flaskup!
FLASKUP_TITLE = 'Flaskup!'
FLASKUP_UPLOAD_FOLDER = '/tmp/flaskup'
FLASKUP_MAX_DAYS = 30
FLASKUP_KEY_LENGTH = 6
FLASKUP_DELETE_KEY_LENGTH = 4
FLASKUP_ADMINS = []

FLASKUP_MAIL_SENDER = 'flaskup@example.com'
FLASKUP_MAIL_SERVER = '127.0.0.1'
FLASKUP_MAIL_PORT = 25

# Flask
DEBUG = False

# Babel
BABEL_DEFAULT_LOCALE = 'en'
BABEL_DEFAULT_TIMEZONE = 'UTC'

# Mail
DEFAULT_MAIL_SENDER = FLASKUP_MAIL_SENDER
MAIL_SERVER = FLASKUP_MAIL_SERVER
MAIL_PORT = FLASKUP_MAIL_PORT

# Create our app
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKUP_CONFIG')

# Babel (i18n)
babel = Babel(app)

# Mail
mail = Mail(app)

# Load dependencies
import flaskup.views
import flaskup.filters
import flaskup.i18n
import flaskup.errorhandler
