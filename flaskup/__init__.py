# -*- coding: utf-8 -*-

from flask import Flask
from flaskext.babel import Babel
from flaskext.mail import Mail


# Flaskup!
UPLOAD_FOLDER = '/tmp/flaskup'
MAX_DAYS = 30

# Flask
DEBUG = False

# Babel
BABEL_DEFAULT_LOCALE = 'en'
BABEL_DEFAULT_TIMEZONE = 'UTC'

# Mail
DEFAULT_MAIL_SENDER = 'flaskup@example.com'

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
