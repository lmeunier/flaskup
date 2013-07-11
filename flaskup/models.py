import os
import uuid
import simplejson
import shutil
from datetime import date, timedelta
from werkzeug import secure_filename
from flask import abort, render_template
from flaskup import app
from flaskup.utils import send_mail
from flaskup.jsonutils import date_encoder, date_decoder


class SharedFile():
    """
    The SharedFile class.
    """

    _GEN_KEY_ATTEMPTS = 10
    _JSON_FILENAME = '.data.json'

    @classmethod
    def gen_key(cls):
        """
        Generate a unique and unpredictable key to identify the file.
        """
        count = 0
        while count < cls._GEN_KEY_ATTEMPTS:
            key = uuid.uuid4().hex[:app.config['FLASKUP_KEY_LENGTH']]
            relative_path = cls.key_to_path(key)
            path = os.path.join(app.config['FLASKUP_UPLOAD_FOLDER'], relative_path)
            if not os.path.exists(path):
                return key

        # unable to find an unused key after 10 attempts
        raise Exception("Unable to generate a unique key after %s attempts." %
                        cls._GEN_KEY_ATTEMPTS)

    @classmethod
    def key_to_path(cls, key):
        """
        Convert a key to a relative path in the filesystem.

        This is where you can change the way files are saved an retrieved.
        If you change this function, old links will be unusable.
        """
        relative_path = os.path.join(key[0], key[1], key)
        return relative_path

    @classmethod
    def get(cls, key):
        """
        Get file informations for the given key.
        """
        relative_path = cls.key_to_path(key)
        path = os.path.join(app.config['FLASKUP_UPLOAD_FOLDER'], relative_path)
        with open(os.path.join(path, key + cls._JSON_FILENAME)) as json_file:
            infos = simplejson.load(json_file, object_hook=date_decoder)
            return cls(**infos)

    @classmethod
    def get_or_404(cls, key):
        """
        Same as get(key), but raise a 404 error if the shared file
        is no found.
        """
        try:
            return cls.get(key)
        except IOError:
            abort(404)

    @classmethod
    def find_all(cls):
        """
        List all shared files.
        """
        upload_folder = app.config['FLASKUP_UPLOAD_FOLDER']
        for root, dirs, files in os.walk(upload_folder):
            current_dir = os.path.basename(root)
            if current_dir + cls._JSON_FILENAME in files:
                key = current_dir
                yield cls.get(key)

    def __init__(self, *args, **kwargs):
        """
        Create a new instance of a SharedFile object.

        This function does not store the uploaded file on disk. You must
        call the save() method to store the file.
        """
        # default values for instance attributes
        self.filename = kwargs.get('filename')
        self.key = kwargs.get('key')
        self.path = kwargs.get('path')
        self.upload_date = kwargs.get('upload_date', date.today())
        self.expire_date = kwargs.get('expire_date', date.today())
        self.delete_key = kwargs.get('delete_key')
        self.remote_ip = kwargs.get('remote_ip')
        self.size = kwargs.get('size', 0)
        self.password_identifier = kwargs.get('password_identifier')

    def save(self, notify=True):
        """
        Save the uploaded file on disk.
        """
        # store the upload file on disk
        self.filename = secure_filename(self.upload_file.filename)
        self.key = self.gen_key()
        self.relative_path = self.key_to_path(self.key)
        path = os.path.join(app.config['FLASKUP_UPLOAD_FOLDER'], self.relative_path)
        os.makedirs(path)
        self.upload_file.save(os.path.join(path, self.filename))
        self.size = os.path.getsize(os.path.join(path, self.filename))

        # generate a unique key needed to delete the file
        self.delete_key = uuid.uuid4().hex[:app.config['FLASKUP_DELETE_KEY_LENGTH']]

        # number of days to keep the file
        self.expire_date = date.today() + timedelta(app.config['FLASKUP_MAX_DAYS'])

        # store informations to keep with the file
        infos = {}
        infos['filename'] = self.filename
        infos['key'] = self.key
        infos['path'] = self.relative_path
        infos['upload_date'] = date.today()
        infos['expire_date'] = self.expire_date
        infos['delete_key'] = self.delete_key
        infos['remote_ip'] = self.remote_ip
        infos['size'] = self.size
        infos['password_identifier'] = self.password_identifier
        path = os.path.join(app.config['FLASKUP_UPLOAD_FOLDER'], self.relative_path)
        with open(os.path.join(path, self.key + self._JSON_FILENAME), 'w') as json_file:
            simplejson.dump(infos, json_file, cls=date_encoder)

        # notify admins
        if 'add' in app.config['FLASKUP_NOTIFY'] and notify:
            subject = render_template('emails/notify_add_subject.txt', f=self)
            body = render_template('emails/notify_add_body.txt', f=self)
            send_mail(subject, body, app.config['FLASKUP_ADMINS'])

    def delete(self, notify=True):
        """
        Remove the folder where the shared file is stored.
        """
        shutil.rmtree(os.path.join(app.config['FLASKUP_UPLOAD_FOLDER'], self.path))

        # notify admins
        if 'delete' in app.config['FLASKUP_NOTIFY'] and notify:
            subject = render_template('emails/notify_delete_subject.txt', f=self)
            body = render_template('emails/notify_delete_body.txt', f=self)
            send_mail(subject, body, app.config['FLASKUP_ADMINS'])


class NginxUploadFile(object):
    def __init__(self, filename, path, content_type=None, size=None):
        self.filename = filename
        self.path = path
        self.content_type = content_type
        self.size = size

    def save(self, dst):
        shutil.move(self.path, dst)
