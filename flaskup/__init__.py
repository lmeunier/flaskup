# -*- coding: utf-8 -*-

import os

from flask import Flask
from flaskext.babel import Babel
from flask.ext.assets import Environment
from webassets.loaders import YAMLLoader
from flask_mail import Mail


# Flaskup!
FLASKUP_TITLE = 'Flaskup!'
FLASKUP_UPLOAD_FOLDER = '/tmp/flaskup'
FLASKUP_MAX_DAYS = 30
FLASKUP_KEY_LENGTH = 6
FLASKUP_DELETE_KEY_LENGTH = 4
FLASKUP_ADMINS = []
FLASKUP_NOTIFY = []
FLASKUP_NGINX_UPLOAD_MODULE_ENABLED = False
FLASKUP_NGINX_UPLOAD_MODULE_STORE = None
FLASKUP_MAX_CONTACTS = 10
FLASKUP_UPLOAD_PASSWORDS = []
FLASKUP_UPLOAD_PASSWORDS_CHECK = lambda a, b: a == b

# Flask
DEBUG = False
SECRET_KEY = None

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


assert app.config['SECRET_KEY'] is not None, \
    "You must define SECRET_KEY"
assert app.config['FLASKUP_MAX_DAYS'] > 0
assert app.config['FLASKUP_KEY_LENGTH'] >= 1 \
    and app.config['FLASKUP_KEY_LENGTH'] <= 32
assert app.config['FLASKUP_DELETE_KEY_LENGTH'] >= 1 \
    and app.config['FLASKUP_DELETE_KEY_LENGTH'] <= 32
assert os.access(app.config['FLASKUP_UPLOAD_FOLDER'], os.W_OK), \
    "No write access to '%s'" % app.config['FLASKUP_UPLOAD_FOLDER']
if app.config['FLASKUP_NGINX_UPLOAD_MODULE_ENABLED']:
    assert app.config['FLASKUP_NGINX_UPLOAD_MODULE_STORE'] is not None, \
        "You must define FLASKUP_NGINX_UPLOAD_MODULE_STORE"
    assert not app.config['FLASKUP_NGINX_UPLOAD_MODULE_STORE'] == '', \
        "You must define FLASKUP_NGINX_UPLOAD_MODULE_STORE"
assert isinstance(app.config['FLASKUP_MAX_CONTACTS'], int) and \
    app.config['FLASKUP_MAX_CONTACTS'] >= 0, \
    "FLASKUP_MAX_CONTACTS must be an integer, greater than or equal to 0"


# Babel (i18n)
babel = Babel(app)

# Mail
mail = Mail(app)

# Flask-Assets
assets_config = YAMLLoader(
    os.path.join(os.path.dirname(__file__), 'assets.yaml')
).load_environment()
assets = Environment(app)
assets.auto_build = not app.config['ASSETS_DEBUG']
assets.url_expire = assets_config.url_expire
assets.cache = assets_config.cache
assets.manifest = assets_config.manifest
assets.register(assets_config._named_bundles)

# Load dependencies
import flaskup.views
import flaskup.filters
import flaskup.i18n
import flaskup.errorhandler
