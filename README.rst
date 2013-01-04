Flaskup! -- A simple Flask application to share files
=====================================================

Overview
--------

Flaskup! is a simple Flask application to share files with your friends. You
upload files through an HTML form, and you get back a link to download the file.
You can do whatever you want with the link (copy it in an email or in your
prefered chat app, it's up to you).

Requirements
------------

- Python 2.6 (may work with other versions but not tested, feedbacks are welcome)
- Flask
- Flask-Babel
- Flask-Mail
- simplejson

Installation
------------

- Download and install Flaskup!:

  ::

    wget http://git.deltalima.net/flaskup/snapshot/flaskup-VERSION.tar.gz
    tar xzf flaskup-VERSION.tar.gz
    cd flaskup-VERSION
    python setup.py install

- or install from PyPI:

  ::

    pip install flaskup

- Use your favorite WSGI server to run Flaskup! (the WSGI application is **flaskup:app**). For example, to use Flaskup! with Gunicorn:

  ::

    gunicorn --bind=127.0.0.1:8001 flaskup:app

- Alternatively, you can start Flaskup! with the builtin Flask webserver (for testing or developpement only).

  create a file `run-server.py`:

  ::

    from flaskup import app
    app.run()

  run it:

  ::

    python run-server.py

Configuration
-------------

You *MUST* set the environment variable FLASKUP_CONFIG that point to a valid
python file. In this file you will be able to customize the configuration for
Flaskup!, Flask and the Flask extensions.

Flaskup!
~~~~~~~~

- `FLASKUP_TITLE`: personnalize the title of this webapp (default: 'Flaskup!')
- `FLASKUP_UPLOAD_FOLDER`: the root folder where you want to store uploaded files (default: /tmp/flaskup).
- `FLASKUP_MAX_DAYS`: the maximum number of days a file will be available, the file will be deleted after FLASKUP_MAX_DAYS days (default: 30).
- `FLASKUP_KEY_LENGTH`: the lenght of the generated key used to identify a file (default: 6 -- more than 2 billions keys)
- `FLASKUP_DELETE_KEY_LENGTH`: the length of the generated key used to authenticate the owner of a file before deleting it (default: 4 -- more than 1 million keys)
- `FLASKUP_ADMINS`: list with email address of the administrators of Flaskup!, this is currently used only to send mails when an error occurs (default: [], empty list)
- `FLASKUP_NOTIFY`: list all actions that should send an email notification to the admins (default: [], no notification)

  - `add`: a new file has been uploaded
  - `delete`: a file has been deleted

Flask
~~~~~

http://flask.pocoo.org/docs/config/#builtin-configuration-values

You must at least define the SECRET_KEY. To generate a good secret key, you can use a cryptographic random generator:

::

  >>> import os
  >>> os.urandom(24)
  '_\x12\xab\x90D\xc4\xfd{\xd9\xe2\xf3-\xa8\xd3\x1d\x1ej\x8b\x13x\x8ce\xc5\xe0'


I18N (Flask-Babel)
~~~~~~~~~~~~~~~~~~

http://packages.python.org/Flask-Babel/#configuration

Mail notification (Flask-Mail)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

http://packages.python.org/flask-mail/#configuring-flask-mail


Example configuration file
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  # -*- coding: utf-8 -*-

  DEBUG = True
  SECRET_KEY = '_\x12\xab\x90D\xc4\xfd{\xd9\xe2\xf3-\xa8\xd3\x1d\x1ej\x8b\x13x\x8ce\xc5\xe0'
  FLASKUP_UPLOAD_FOLDER = '/srv/flaskup/data'
  FLASKUP_MAX_DAYS = 10
  FLASKUP_KEY_LENGTH = 4
  DEFAULT_MAIL_SENDER = 'flaskup@example.com'
  FLASKUP_ADMINS = ['admin@example.com', 'admin@example.org']
  FLASKUP_NOTIFY = ['add']

Delete expired files
--------------------

Flaskup! comes with the command line tool ``flaskup``. This tool is a generic python script to call actions. Currently the only available action is `clean`.

::

  . /path/to/env/bin/activate
  export FLASKUP_CONFIG=/path/to/my/flaskup_config.py
  flaskup clean 

Credits
-------

Flaskup! is maintained by `Laurent Meunier <http://www.deltalima.net/>`_.

Licenses
--------

Flaskup! is Copyright (c) 2012 Laurent Meunier. It is free software, and may be redistributed under the terms specified in the LICENSE file (a 3-clause BSD License).

Flaskup! uses `Bootstrap <http://twitter.github.com/bootstrap/>`_ (`Apache License v2.0 <http://www.apache.org/licenses/LICENSE-2.0>`_) and `jQuery <http://jquery.com/>`_ (`MIT or GPLv2 License <http://jquery.org/license/>`_).

