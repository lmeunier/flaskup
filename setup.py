import os
import re
import codecs
import pojson
from setuptools import setup
from distutils import cmd
from distutils.errors import DistutilsOptionError
from babel.messages import frontend as babel

version = '0.3'


def parse_requirements(file_name):
    requirements = []
    for line in open(file_name, 'r').read().split('\n'):
        if re.match(r'(\s*#)|(\s*$)', line):
            continue
        if re.match(r'\s*-e\s+', line):
            requirements.append(re.sub(r'\s*-e\s+.*#egg=(.*)$', r'\1', line))
        elif re.match(r'\s*-f\s+', line):
            pass
        else:
            requirements.append(line)

    return requirements


class compile_pojson(cmd.Command):
    description = 'Compile .po files to .json files using `pojson`'
    user_options = [
        ('input-dir', 'i', 'path to the input dir'),
        ('output-dir', 'o', 'path to the output dir'),
    ]

    def initialize_options(self):
        self.input_dir = None
        self.output_dir = None

    def finalize_options(self):
        if not self.input_dir:
            raise DistutilsOptionError('you must specify the input dir')

        if not self.output_dir:
            raise DistutilsOptionError('you must specify the output dir')

    def run(self):
        for locale in os.listdir(self.input_dir):
            po_file = os.path.join(self.input_dir, locale, 'LC_MESSAGES',
                                   'messages.po')
            if os.path.exists(po_file):
                json_data = pojson.convert(po_file)
                json_file = os.path.join(self.output_dir, locale + '.json')
                with codecs.open(json_file, 'w', encoding='utf8') as out_file:
                    print "compiling catalog '{}' to '{}'".format(po_file,
                                                                  json_file)
                    out_file.write(json_data)


setup(
    name='flaskup',
    version=version,
    description='A simple Flask application to share files.',
    long_description=__doc__,
    author='Laurent Meunier',
    author_email='laurent@deltalima.net',
    license='BSD',
    url='http://git.deltalima.net/flaskup/',
    download_url='http://git.deltalima.net/flaskup/snapshot/flaskup-'
        + version + '.tar.gz',
    packages=['flaskup'],
    include_package_data=True,
    zip_safe=False,
    install_requires=parse_requirements("requirements.txt"),
    entry_points={
        'console_scripts': [
            'flaskup = flaskup.console:main',
        ],
    },
    cmdclass={
        'extract_messages': babel.extract_messages,
        'init_catalog': babel.init_catalog,
        'update_catalog': babel.update_catalog,
        'compile_catalog': babel.compile_catalog,
        'compile_pojson': compile_pojson,
    },
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Communications :: File Sharing',
        'Topic :: Internet',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ]
)
