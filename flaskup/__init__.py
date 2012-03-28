# -*- coding: utf-8 -*-

from flask import Flask

DEBUG = False
UPLOAD_FOLDER = '/tmp/flaskup'
MAX_DAYS = 30

# Create our app
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKUP_CONFIG')

# Load dependencies 
import flaskup.views
import flaskup.filters

