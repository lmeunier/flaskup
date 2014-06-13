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

- Python 2.7 (may work with other versions but not tested, feedbacks are welcome)
- Flask
- Flask-Babel
- Flask-Mail
- simplejson


Installation
------------

- Install from PyPI:

  ::

    pip install flaskup

- or directly from the Git repository (to have latest features):

  ::

    git clone https://github.com/lmeunier/flaskup.git
    cd flaskup
    python setup.py install


Configuration
-------------

You *MUST* set the environment variable FLASKUP_CONFIG that point to a valid
python file. In this file you will be able to customize the configuration for
Flaskup!, Flask and the Flask extensions.

Flaskup!
~~~~~~~~

- `FLASKUP_TITLE`: personnalize the title of this webapp (default: 'Flaskup!')
- `FLASKUP_UPLOAD_FOLDER`: the root folder where you want to store uploaded
  files (default: /tmp/flaskup).
- `FLASKUP_MAX_DAYS`: the maximum number of days a file will be available, the
  file will be deleted after FLASKUP_MAX_DAYS days (default: 30).
- `FLASKUP_MAX_CONTACTS`: limit contacts number, if the user gives more
  contacts, they will be silently discarded (default: 10 ; 0 means 'no
  contacts' and the textarea won't be displayed)
- `FLASKUP_KEY_LENGTH`: the lenght of the generated key used to identify a file
  (default: 6 -- more than 2 billions keys)
- `FLASKUP_DELETE_KEY_LENGTH`: the length of the generated key used to
  authenticate the owner of a file before deleting it (default: 4 -- more than
  1 million keys)
- `FLASKUP_ADMINS`: list with email address of the administrators of Flaskup!,
  this is currently used only to send mails when an error occurs (default: [],
  empty list)
- `FLASKUP_NOTIFY`: list all actions that should send an email notification to
  the admins (default: [], no notification)

  - `add`: a new file has been uploaded
  - `delete`: a file has been deleted

- `FLASKUP_NGINX_UPLOAD_MODULE_ENABLED`: indicate whether you want to enable
  support for the Nginx upload-module (default: `False`)
- `FLASKUP_NGINX_UPLOAD_MODULE_STORE`: must be set to the `upload_store` of the
  Nginx upload-module (default: `None`)
- `FLASKUP_UPLOAD_PASSWORDS`: a list of tuples, each tuple contains a password
  and an identifier (default: [], no password required)
- `FLASKUP_UPLOAD_PASSWORDS_CHECK`: method to check a submitted password against
  passwords in `FLASKUP_UPLOAD_PASSWORDS` (default: use cleartext passwords)

Flask
~~~~~

http://flask.pocoo.org/docs/config/#builtin-configuration-values

You must at least define the SECRET_KEY. To generate a good secret key, you can
use a cryptographic random generator:

::

  >>> import os
  >>> os.urandom(24)
  '_\x12\xab\x90D\xc4\xfd{\xd9\xe2\xf3-\xa8\xd3\x1d\x1ej\x8b\x13x\x8ce\xc5\xe0'


I18N (Flask-Babel)
~~~~~~~~~~~~~~~~~~

https://pythonhosted.org/Flask-Babel/#configuration

Mail notification (Flask-Mail)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

https://pythonhosted.org/Flask-Mail/#configuring-flask-mail

Example configuration file
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  # -*- coding: utf-8 -*-

  from passlib.hash import bcrypt

  DEBUG = True
  SECRET_KEY = '_\x12\xab\x90D\xc4\xfd{\xd9\xe2\xf3-\xa8\xd3\x1d\x1ej\x8b\x13x\x8ce\xc5\xe0'
  FLASKUP_UPLOAD_FOLDER = '/srv/flaskup/data'
  FLASKUP_MAX_DAYS = 10
  FLASKUP_KEY_LENGTH = 4
  MAIL_DEFAULT_SENDER = 'flaskup@example.com'
  FLASKUP_ADMINS = ['admin@example.com', 'admin@example.org']
  FLASKUP_NOTIFY = ['add', 'delete']
  FLASKUP_UPLOAD_PASSWORDS = [
    ('$2a$12$oIWeziyq4wjF08gntfU4w.AQZfYbbQoK7y13ParN83G7ta.qtN2.e', 'pw1'),
    ('$2a$12$zQ/hzog/iYr49fbo0mitS.y9f.uHP.7IyqWgk5/S1Ict50HRl4XxW', 'pw2'),
  ]
  FLASKUP_UPLOAD_PASSWORDS_CHECK = bcrypt.verify

Run Flaskup!
------------

- Use your favorite WSGI server to run Flaskup! (the WSGI application is
  **flaskup:app**). For example, to use Flaskup! with Gunicorn:

  ::

    gunicorn --bind=127.0.0.1:8001 flaskup:app

- Alternatively, you can start Flaskup! with the builtin Flask webserver (for
  testing or developpement only).

  create a file `run-server.py`:

  ::

    from flaskup import app
    app.run()

  run it:

  ::

    python run-server.py


Delete expired files
--------------------

Flaskup! comes with the command line tool ``flaskup``. This tool is a generic
python script to call actions. Currently the only available action is `clean`.

::

  . /path/to/env/bin/activate
  export FLASKUP_CONFIG=/path/to/my/flaskup_config.py
  flaskup clean

Password protection
-------------------

The password protection in Flaskup! is a very simple mechanism to force users
to submit a valid password when they upload a file.

List of valid passwords
~~~~~~~~~~~~~~~~~~~~~~~

Valid passwords are stored in a tuple (with a password identifier), those
tuples are stored as a list in `FLASKUP_UPLOAD_PASSWORDS`. If
`FLASKUP_UPLOAD_PASSWORDS` is empty, then no valid password are required and
anybody can upload a file.

::

  FLASKUP_UPLOAD_PASSWORDS = [
    ('password1', 'identifier for password 1'),
    ('secretpassword2', 'identifier for password 2'),
  ]

The password identifier is stored in the `*.data.json` file next to the
uploaded file. This permits to identify which password was used to upload the
file.

A password is never required to download files, only to upload them.

Use hashed passwords
~~~~~~~~~~~~~~~~~~~~

By default, Flaskup! will treat passwords from `FLASKUP_UPLOAD_PASSWORDS` as
cleartext (not hashed). If you want to put hashed passwords in
`FLASKUP_UPLOAD_PASSWORDS`, you must define `FLASKUP_UPLOAD_PASSWORDS_CHECK`.

`FLASKUP_UPLOAD_PASSWORDS_CHECK` must be a reference to a method that accepts
two arguments: the user submitted password and the hashed password (from
`FLASKUP_UPLOAD_PASSWORDS`), and then returns `True` if passwords match, else
`False`.

::

  from passlib.hash import bcrypt

  FLASKUP_UPLOAD_PASSWORDS = [
    ('$2a$12$oIWeziyq4wjF08gntfU4w.AQZfYbbQoK7y13ParN83G7ta.qtN2.e', 'pw1'),
    ('$2a$12$zQ/hzog/iYr49fbo0mitS.y9f.uHP.7IyqWgk5/S1Ict50HRl4XxW', 'pw2'),
  ]
  FLASKUP_UPLOAD_PASSWORDS_CHECK = bcrypt.verify

Nginx Upload Module
-------------------

If you are using `Nginx <http://nginx.org/>`_ with the `upload-module
<http://wiki.nginx.org/HttpUploadModule>`_, you can configure it to efficiently
upload files to Flaskup!. Using this module is recommended when you need to
deal with large files: the whole POST is not decoded in Python and the uploaded
file is moved just one time (with the normal file upload mechanism the file is
re-sent from Nginx to your WSGI server, and then it is copied to the final
destination).


Configure Flaskup!
~~~~~~~~~~~~~~~~~~

You must define the two following configuration values:

- `FLASKUP_NGINX_UPLOAD_MODULE_ENABLED`: must be set to `True`
- `FLASKUP_NGINX_UPLOAD_MODULE_STORE`: must be set to the `upload_store` of the
  upload-module

Example configuration::

  FLASKUP_NGINX_UPLOAD_MODULE_ENABLED = True
  FLASKUP_NGINX_UPLOAD_MODULE_STORE = /tmp/nginx_upload_module


Configure Nginx
~~~~~~~~~~~~~~~

- be sure that you compiled Nginx with the upload-module
- create a folder where uploaded files will be stored, preferably on the same
  disk or partition as `FLASKUP_UPLOAD_FOLDER` to avoid unnecessary I/O
  operations (this folder is named `upload_store` in your Nginx config)
- check permissions on the `upload_store` folder: users running Nginx and
  Flaskup! must have read/write permissions
- edit your configuration file (add the `/upload` location)

Example configuration::

  server {
      listen [::]:80;
      server_name "flaskup.example.com";
      client_max_body_size 2g;

      access_log /var/log/nginx/flaskup_access.log combined;
      error_log  /var/log/nginx/flaskup_error.log;

      proxy_set_header X-Real-IP $remote_addr;
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_set_header Host $http_host;

      location /static/ {
              alias   /path/to/env/lib/python2.7/site-packages/flaskup/static/;
      }
      location = /upload {
              upload_pass             @upstream;
              upload_store            /tmp/nginx_upload_module;
              upload_store_access     user:rw;

              upload_set_form_field   $upload_field_name.name "$upload_file_name";
              upload_set_form_field   $upload_field_name.path "$upload_tmp_path";

              upload_pass_form_field  "^myemail$|^mycontacts$";
              upload_cleanup          400-599;
      }
      location / {
          proxy_pass http://127.0.0.1:8000;
      }
      location @upstream {
          proxy_pass http://127.0.0.1:8000;
      }
  }


Credits
-------

Flaskup! is maintained by `Laurent Meunier <http://www.deltalima.net/>`_.


Licenses
--------

Flaskup! is Copyright (c) 2012 Laurent Meunier. It is free software, and may be
redistributed under the terms specified in the LICENSE file (a 3-clause BSD
License).

Flaskup! uses `Bootstrap <http://twitter.github.com/bootstrap/>`_ (`Apache
License v2.0 <http://www.apache.org/licenses/LICENSE-2.0>`_) and `jQuery
<http://jquery.com/>`_ (`MIT or GPLv2 License <http://jquery.org/license/>`_).
