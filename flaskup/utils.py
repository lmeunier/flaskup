# -*- coding: utf-8 -*-

import os, base64, simplejson, uuid, shutil
from datetime import date, timedelta
from werkzeug import secure_filename
from flask import render_template
from flaskext.babel import gettext as _
from flask_mail import Message
from flaskup.jsonutils import date_encoder, date_decoder
from flaskup import app, mail


JSON_FILENAME = 'data.json'

def key_to_path(key):
    """
    Convert a key to a relative path in the filesystem.

    This is where you can change the way files are saved an retrieved.
    If you change this function, old links will be unusable.
    """
    relative_path = os.path.join(key[0], key[1], key)
    return relative_path

def gen_key(file):
    count = 0
    while count < 10:
        key = uuid.uuid4().hex[:app.config['FLASKUP_KEY_LENGTH']]
        relative_path = key_to_path(key)
        path = os.path.join(app.config['FLASKUP_UPLOAD_FOLDER'], relative_path)
        if not os.path.exists(path):
            return key
    # TODO
    # unable to find an unused key after 10 attempts
    # should log this or email admin

def save_file(file):
    filename = secure_filename(file.filename)
    if filename == JSON_FILENAME:
        filename = '_' + filename
    if not filename:
        raise Exception(_(u'You must choose a file.'))
    key = gen_key(file)
    relative_path = key_to_path(key)
    path = os.path.join(app.config['FLASKUP_UPLOAD_FOLDER'], relative_path)
    os.makedirs(path)
    file.save(os.path.join(path, filename))
    return relative_path, filename, key

def get_file_info(key):
    relative_path = key_to_path(key)
    path = os.path.join(app.config['FLASKUP_UPLOAD_FOLDER'], relative_path)
    with open(os.path.join(path, JSON_FILENAME)) as json_file:
        infos = simplejson.load(json_file, object_hook=date_decoder)
    return infos

def remove_file(key):
    path = key_to_path(key)
    upload_folder = app.config['FLASKUP_UPLOAD_FOLDER']
    shutil.rmtree(os.path.join(upload_folder, path))

def process_request(request):
    """
    This is the big function where almost all processing is done:
    - save the uploaded file on disk
    - create the data.json file (where all metadatas about the uploaded file
    is stored)
    - send emails
    """

    if not 'myfile' in request.files:
        raise Exception(_(u'You must choose a file.'))

    # process file
    f = request.files['myfile']
    if not file:
        raise Exception(_(u'You must choose a file.'))
    else:
        # save file
        relative_path, filename, key = save_file(f)
        delete_key = uuid.uuid4().hex[:app.config['FLASKUP_DELETE_KEY_LENGTH']]

        # number of days to keep the file
        expire_days = app.config['FLASKUP_MAX_DAYS']
        if 'days' in request.form:
            expire_days = int(request.form['days'])
            if expire_days > app.config['FLASKUP_MAX_DAYS']:
                expire_days = app.config['FLASKUP_MAX_DAYS']
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
        infos['delete_key' ] = delete_key
        path = os.path.join(app.config['FLASKUP_UPLOAD_FOLDER'], relative_path)
        with open(os.path.join(path, JSON_FILENAME), 'w') as json_file:
            simplejson.dump(infos, json_file, cls=date_encoder)

    # notify the uploader of the file 
    if 'myemail' in request.form:
        myemail = request.form['myemail'].strip()
        if myemail:
            subject = render_template('emails/notify_me_subject.txt',
                                      infos=infos,
                                      recipient=myemail)
            body = render_template('emails/notify_me_body.txt',
                                   infos=infos,
                                   recipient=myemail)
            send_mail(subject, body, myemail)

    # notify contacts
    # TODO limit the number of contacts
    if 'mycontacts' in request.form and myemail:
        mycontacts = request.form['mycontacts']
        if mycontacts:
            for contact in [c.strip() for c in mycontacts.splitlines()]:
                if contact:
                    subject = render_template('emails/notify_contact_subject.txt',
                                              infos=infos,
                                              sender=myemail,
                                              recipient=contact)
                    body = render_template('emails/notify_contact_body.txt',
                                           infos=infos,
                                           sender=myemail,
                                           recipient=contact)
                    send_mail(subject, body, contact)

    return infos

def send_mail(subject, body, recipient):
    # remove new lines from subject
    subject = ' '.join(subject.strip().splitlines())
    msg = Message(subject, recipients=[recipient])
    msg.body = body

    try:
        mail.send(msg)
    except:
        # this is likely to be a bad recipient address
        # ... or a failure in the MTA
        # in any case, we don't want to bother the user with these errors
        # so we fail silently
        pass
