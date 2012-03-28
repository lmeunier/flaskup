# -*- coding: utf-8 -*-

import os, base64, simplejson, uuid
from datetime import datetime, timedelta
from werkzeug import secure_filename
from flask import render_template, url_for, redirect, request, abort
from flask import send_file
from flaskup import app
from flaskup.jsonencoder import datetime_encoder, datetime_decoder

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
        infos = simplejson.load(json_file, object_hook=datetime_decoder)
    return infos
    

@app.route('/')
def show_upload_form():
    return render_template('show_upload_form.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if not 'file' in request.files:
        error = "You must choose a file."
        return render_template('show_upload_form.html', error=error)

    file = request.files['file']
    if file:
        # save file
        relative_path, filename, key = save_file(file)

        # number of days to keep the file
        expire_days = app.config['MAX_DAYS']
        if 'days' in request.form:
            expire_days = int(request.form['days'])
            if expire_days > app.config['MAX_DAYS']:
                expire_days = app.config['MAX_DAYS']
        expire_date = datetime.now() + timedelta(expire_days)

        # store informations to keep with the file
        infos = {}
        infos['filename'] = filename
        infos['key'] = key
        infos['path'] = relative_path
        infos['upload_client'] = request.environ['REMOTE_ADDR']
        infos['upload_date'] = datetime.now()
        infos['expire_date'] = expire_date
        path = os.path.join(app.config['UPLOAD_FOLDER'], relative_path)
        with open(os.path.join(path, JSON_FILENAME), 'w') as json_file:
            simplejson.dump(infos, json_file, cls=datetime_encoder)

        # all is successful, redirect the user
        return redirect(url_for('show_uploaded_file', key=key))
    else:
        error = "You must choose a file."
        return render_template('show_upload_form.html', error=error)

@app.route('/uploaded/<key>/')
def show_uploaded_file(key):
    try:
        infos = get_file_info(key)
    except IOError:
        abort(404)
    return render_template('show_uploaded_file.html', infos=infos)

@app.route('/get/<key>/')
def show_get_file(key):
    try:
        infos = get_file_info(key)
    except IOError:
        abort(404)
    return render_template('show_get_file.html', infos=infos)

@app.route('/get/<key>/<filename>')
def get_file(key, filename):
    infos = get_file_info(key)
    if infos['filename'] == filename:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], infos['path'],
                                filename)
        return send_file(filepath, as_attachment=True,
                         attachment_filename=filename)
    else:
        abort(404)

