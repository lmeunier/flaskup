# -*- coding: utf-8 -*-

import os
from flask import render_template, url_for, redirect, request, abort
from flask import send_file, make_response
from flaskup import app
from flaskup.utils import process_request, get_file_info, remove_file

@app.route('/')
def show_upload_form():
    return render_template('show_upload_form.html')

@app.route('/upload-xhr', methods=['POST'])
def upload_file_xhr():
    """
    This view is dedicated to javascript uploads via XHR.
    Non-javascript browser will use 'upload_file()'.
    """
    try:
        infos = process_request(request)
    except Exception as e:
        return e, 400
    return url_for('show_uploaded_file', key=infos['key'])

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        infos = process_request(request)
    except Exception as e:
        return render_template('show_upload_form.html', error=e)
    return redirect(url_for('show_uploaded_file', key=infos['key'])) 

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
    try:
        infos = get_file_info(key)
    except IOError:
        abort(404)

    if not infos['filename'] == filename:
        abort(404)

    filepath = os.path.join(app.config['FLASKUP_UPLOAD_FOLDER'],
                            infos['path'], filename)
    if not os.path.isfile(filepath):
        abort(404)

    # add the 'Content-Length' header
    # browsers can show a progress bar
    filesize = str(os.path.getsize(filepath))
    response = make_response(send_file(filepath, as_attachment=True,
                             attachment_filename=filename))
    response.headers['Content-Length'] = filesize

    return response

@app.route('/delete/<key>/<secret>/')
def show_delete_file(key, secret):
    try:
        infos = get_file_info(key)
    except IOError:
        abort(404)
    if secret != infos['delete_key']:
        abort(404)
    return render_template('show_delete_file.html', infos=infos)

@app.route('/delete_confirmed/<key>/<secret>/')
def show_confirm_delete_file(key, secret):
    try:
        infos = get_file_info(key)
    except IOError:
        abort(404)
    if secret != infos['delete_key']:
        abort(404)

    # effectively delete the file
    remove_file(key)
    return render_template('show_deleted_file.html', infos=infos)
