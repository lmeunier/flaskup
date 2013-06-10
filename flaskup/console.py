# -*- coding: utf-8 -*-

import os
import argparse
from datetime import date
from flaskup.models import SharedFile
from flaskup.filters import filesizeformat


def action_clean(quiet):
    today = date.today()
    count = 0
    deleted_files = []

    for f in SharedFile.find_all():
        if f.expire_date < today:
            f.delete(notify=False)
            count += 1
            deleted_files.append(f)

    if not quiet and count > 0:
        print u'Files deleted: {0}'.format(count)
        for info in deleted_files:
            print u" - '{0}' - {1}".format(os.path.join(info.path, info.filename),
                                           filesizeformat(info.size, True))


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
