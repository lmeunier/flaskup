# -*- coding: utf-8 -*-

import os, sys, argparse
from datetime import date
from flaskup import app, utils

def clean(quiet):
    today = date.today()
    upload_folder = app.config['UPLOAD_FOLDER']
    count = 0
    for root, dirs, files in os.walk(upload_folder):
        if utils.JSON_FILENAME in files:
            try:
                path, key = os.path.split(root)
                infos = utils.get_file_info(key)
                expire_date = infos['expire_date']
                if expire_date < today:
                    utils.remove_file(infos['key'])
                    count += 1
            except Exception as e:
                print >> sys.stderr, "Error for '{0}': {1}".format(root, e)

    if not quiet:
        print 'Files deleted: {0}'.format(count)

def main():
    # parse arguments
    parser = argparse.ArgumentParser(description='Flaskup! command line tool.')
    parser.add_argument('-q', '--quiet',
                        action='store_true',
                        help='quiet, print only errors')
    parser.add_argument('action', choices=['clean'])
    args = parser.parse_args()

    # quiet?
    quiet = args.quiet

    # call function
    from flaskup import console
    action = getattr(console, args.action)
    action(quiet)
