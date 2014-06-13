import re
from setuptools import setup
from babel.messages import frontend as babel

version = '0.3.2'


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


setup(
    name='flaskup',
    version=version,
    description='A simple Flask application to share files.',
    long_description=__doc__,
    author='Laurent Meunier',
    author_email='laurent@deltalima.net',
    license='BSD',
    url='http://git.deltalima.net/flaskup/',
    download_url='http://git.deltalima.net/flaskup/snapshot/flaskup-'+version+'.tar.gz',
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
