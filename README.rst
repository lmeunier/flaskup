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
- Flask >= 0.8
- Flask-Babel >= 0.8
- simplejson

Notes
-----

- Currently, there is nothing in the code that will delete expired files. They will always be available to download.


Installation
------------

- Install Flask! with setup.py (I recommend you to use virtualenv):

  ``python setup.py install``

- Use your favorite WSGI server to run Flaskup! (the WSGI application is **flaskup:app**). For example, to use Flaskup! with Gunicorn:

  ``gunicorn --bind=127.0.0.1:8001 flaskup:app``

- Alternatively, you can start Flaskup! with the builtin Flask webserver (for testing or developpement only).

  create a file `run-server.py`:

  ::

    from flaskup import app
    app.run()
  
  run it:

  ``python run-server.py``

Configuration
-------------

You *MUST* set the environment variable FLASKUP_CONFIG that point to a valid
python file. In this file you will be able to customize the configuration for
Flaskup! and for Flask.

Flask
~~~~~

http://flask.pocoo.org/docs/config/#builtin-configuration-values

Flaskup!
~~~~~~~~

- `UPLOAD_FOLDER`: the root folder where you want to store uploaded files (default: /tmp/flaskup).
- `MAX_DAYS`: the maximim number of days a file will be available, the file will be deleted after MAX_DAYS days (default: 30).

Example configuration file
~~~~~~~~~~~~~~~~~~~~~~~~~~

::
  
  # -*- coding: utf-8 -*-
  
  DEBUG = True
  UPLOAD_FOLDER = '/srv/flaskup/data'
  MAX_DAYS = 10

Delete expired files
--------------------

Flaskup! comes with the command line tool ``flaskup``. This tool is a generic python script to call actions. Currently the only available action is `clean`.

::
  
  $ . /path/to/env/bin/activate
  $ export FLASKUP_CONFIG=/path/to/my/flaskup_config.py
  $ flaskup clean 

TODO
----

- 'delete my file' link
- send email with a link to the download page
- custom error pages
- unit tests

Credits
-------

Flaskup! is maintained by `Laurent Meunier <http://www.deltalima.net/>`_.

License
-------

Flaskup! is Copyright (c) 2012 Laurent Meunier. It is free software, and may be redistributed under the terms specified in the LICENSE file (a 3-clause BSD License).
