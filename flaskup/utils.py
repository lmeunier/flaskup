# -*- coding: utf-8 -*-

import os, base64, simplejson, uuid                                             
from datetime import date, timedelta                                            
from werkzeug import secure_filename
from flaskext.babel import gettext
from flaskup.jsonencoder import date_encoder, date_decoder                      
from flaskup import app                                                         


JSON_FILENAME = 'data.json'

def key_to_path(key):
    """
    Convert a key to a relative path in the filesystem.
    The path contains UPLOAD_FOLDER.

    This is where you can change the way files are saved an retrieved.
    If you change this function, old links will be unusable.
    """
    relative_path = os.path.join(key[0], key[1], key)
    return relative_path

def gen_key(file):
    count = 0
    while count < 10:
        key = uuid.uuid4().hex
        relative_path = key_to_path(key)
        path = os.path.join(app.config['UPLOAD_FOLDER'], relative_path)
        if not os.path.exists(path):
            return key
    # TODO    
    # unable to find a free key after 10 attempts
    # should log this or email admin

def save_file(file):
    filename = secure_filename(file.filename)
    if filename == JSON_FILENAME:
        filename = '_' + filename
    if not filename:
        raise Exception(gettext(u'You must choose a file.'))
    key = gen_key(file) 
    relative_path = key_to_path(key)
    path = os.path.join(app.config['UPLOAD_FOLDER'], relative_path)
    os.makedirs(path)
    file.save(os.path.join(path, filename))
    return relative_path, filename, key

def get_file_info(key):
    relative_path = key_to_path(key)
    path = os.path.join(app.config['UPLOAD_FOLDER'], relative_path)
    with open(os.path.join(path, JSON_FILENAME)) as json_file:
        infos = simplejson.load(json_file, object_hook=date_decoder)
    return infos

def process_file(request):
    if not 'file' in request.files:
        raise Exception(gettext(u'You must choose a file.'))

    f = request.files['file']
    if not file:
        raise Exception(gettext(u'You must choose a file.'))
    else:
        # save file
        relative_path, filename, key = save_file(f)

        # number of days to keep the file
        expire_days = app.config['MAX_DAYS']
        if 'days' in request.form:
            expire_days = int(request.form['days'])
            if expire_days > app.config['MAX_DAYS']:
                expire_days = app.config['MAX_DAYS']
        expire_date = date.today() + timedelta(expire_days)

        # store informations to keep with the file
        infos = {}
        infos['filename'] = filename
        infos['key'] = key
        infos['path'] = relative_path
        infos['upload_client'] = request.environ['REMOTE_ADDR']
        infos['upload_date'] = date.today()
        infos['expire_date'] = expire_date
        infos['expire_days'] = expire_days
        path = os.path.join(app.config['UPLOAD_FOLDER'], relative_path)
        with open(os.path.join(path, JSON_FILENAME), 'w') as json_file:
            simplejson.dump(infos, json_file, cls=date_encoder)

        return infos
