# -*- coding: utf-8 -*-

import os
from flask import render_template, url_for, redirect, request, abort, flash
from flask import send_file, make_response, jsonify
from flaskext.babel import gettext as _
from flaskup import app
from flaskup.utils import send_mail
from flaskup.models import SharedFile, NginxUploadFile


@app.route('/')
def show_upload_form():
    return render_template('show_upload_form.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    remote_ip = request.environ.get('REMOTE_ADDR', None)

    if 'myfile' in request.files and request.files['myfile']:
        # Werkzeug `FileStorage` (normal HTTP Post)
        upload_file = request.files['myfile']
    elif 'myfile.name' in request.form and 'myfile.path' in request.form:
        # Nginx Upload Module
        upload_file = NginxUploadFile(
            filename=request.form['myfile.name'],
            path=request.form['myfile.path']
        )
    else:
        # no upload file
        message = _("The file is required.")
        if request.is_xhr:
            return jsonify(message=message), 400
        else:
            return render_template('show_upload_form.html', error=message)

    shared_file = SharedFile()
    shared_file.upload_file = upload_file
    shared_file.remote_ip = remote_ip
    shared_file.save()

    # notify the user
    myemail = request.form.get('myemail', '').strip()
    if myemail:
        subject = render_template('emails/notify_me_subject.txt',
                                  f=shared_file,
                                  recipient=myemail)
        body = render_template('emails/notify_me_body.txt',
                               f=shared_file,
                               recipient=myemail)
        send_mail(subject, body, [myemail])

    # notify contacts
    # TODO limit the number of contacts
    if 'mycontacts' in request.form and myemail:
        mycontacts = request.form['mycontacts']
        for contact in [c.strip() for c in mycontacts.splitlines()]:
            if contact:
                subject = render_template('emails/notify_contact_subject.txt',
                                          f=shared_file,
                                          sender=myemail,
                                          recipient=contact)
                body = render_template('emails/notify_contact_body.txt',
                                       f=shared_file,
                                       sender=myemail,
                                       recipient=contact)
                send_mail(subject, body, [contact])

    if request.is_xhr:
        return jsonify(url=url_for('show_uploaded_file', key=shared_file.key,
                       secret=shared_file.delete_key))
    else:
        return redirect(url_for('show_uploaded_file', key=shared_file.key,
                        secret=shared_file.delete_key))


@app.route('/uploaded/<key>/<secret>/')
def show_uploaded_file(key, secret):
    shared_file = SharedFile.get_or_404(key)

    if secret != shared_file.delete_key:
        abort(404)

    return render_template('show_uploaded_file.html', f=shared_file)


@app.route('/get/<key>/')
def show_get_file(key):
    shared_file = SharedFile.get_or_404(key)
    return render_template('show_get_file.html', f=shared_file)


@app.route('/get/<key>/<filename>')
def get_file(key, filename):
    shared_file = SharedFile.get_or_404(key)

    if not shared_file.filename == filename:
        abort(404)

    filepath = os.path.join(app.config['FLASKUP_UPLOAD_FOLDER'],
                            shared_file.path, filename)
    if not os.path.isfile(filepath):
        abort(404)

    # add the 'Content-Length' header
    # browsers can show a progress bar
    filesize = str(shared_file.size)
    response = make_response(send_file(filepath, as_attachment=True,
                             attachment_filename=filename))
    response.headers['Content-Length'] = filesize

    return response


@app.route('/delete/<key>/<secret>/', methods=['GET', 'POST'])
def show_delete_file(key, secret):
    shared_file = SharedFile.get_or_404(key)

    if secret != shared_file.delete_key:
        abort(404)

    if request.method == 'POST':
        # delete the file and redirect to the upload form
        shared_file.delete()
        flash(_('Your file have been deleted.'))
        return redirect(url_for('show_upload_form'))

    return render_template('show_delete_file.html', f=shared_file)
