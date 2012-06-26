# -*- coding: utf-8 -*-

import os, sys, argparse
from datetime import date
from flaskup import app, utils

def action_clean(quiet):
    today = date.today()
    upload_folder = app.config['FLASKUP_UPLOAD_FOLDER']
    count = 0
    deleted_files = []
    for root, dirs, files in os.walk(upload_folder):
        if utils.JSON_FILENAME in files:
            try:
                path, key = os.path.split(root)
                infos = utils.get_file_info(key)
                expire_date = infos['expire_date']
                if expire_date < today:
                    utils.remove_file(infos['key'])
                    count += 1
                    deleted_files.append(infos)
            except Exception as e:
                print >> sys.stderr, u"Error for '{0}': {1}".format(root, e)

    if not quiet and count > 0:
        print u'Files deleted: {0}'.format(count)
        for info in deleted_files:
            print u" - '{0}'".format(os.path.join(info['path'], info['filename']))

def list_actions():
    from flaskup import console
    attributes = dir(console)
    
    actions = []
    for attribute in attributes:
        if attribute.startswith('action_'):
            actions.append(attribute[7:])
    return actions

def main():
    # parse arguments
    parser = argparse.ArgumentParser(description='Flaskup! command line tool.')
    parser.add_argument('-q', '--quiet',
                        action='store_true',
                        help='quiet, print only errors')
    choices = list_actions()
    parser.add_argument('action', choices=choices)
    args = parser.parse_args()

    # quiet?
    quiet = args.quiet

    # call function
    from flaskup import console
    action = getattr(console, 'action_' + args.action)
    action(quiet)
