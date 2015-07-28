#!/usr/bin/env python
"""
gitlab_email_list.py
====================

Dump a list of all GitLab user email addresses.

If you have ideas for improvements, or want the latest version, it's at:
<https://github.com/jantman/gitlab-scripts/blob/master/gitlab_email_list.py>

Usage
-----

1. Export your GitLab Private API token as GITLAB_TOKEN, or you will be prompted
   for it interactively.
2. Run the script:

    gitlab_email_list.py http://gitlab.example.com

Requirements
-------------

python-gitlab (tested with 0.9.2; `pip install python-gitlab`)

WARNING - Note that per https://github.com/gpocentek/python-gitlab/issues/63
python-gitlab 0.9.2 doesn't handle paginated responses, so it will silently
disregard anything past the 20th result.

Copyright and License
----------------------

Copyright 2015 Jason Antman <jason@jasonantman.com> <http://www.jasonantman.com>

    This file is part of gitlab-scripts.

    gitlab-scripts is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    gitlab-scripts is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with gitlab-scripts.  If not, see <http://www.gnu.org/licenses/>.

Changelog
----------

2015-07-28 Jason Antman <jason@jasonantman.com>:
  - initial version of script
"""

import sys
import argparse
import logging
import gitlab
import os
import json

FORMAT = "[%(levelname)s %(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT)
logger = logging.getLogger()

# suppress requests internal logging
requests_log = logging.getLogger("requests")
requests_log.setLevel(logging.WARNING)
requests_log.propagate = True

gitlab_log = logging.getLogger("gitlab")
gitlab_log.setLevel(logging.WARNING)
gitlab_log.propagate = True

class GitLabEmailList:
    """sync local ssh authorized_keys to GitLab"""

    def __init__(self, url, apikey):
        """connect to GitLab"""
        logger.debug("Connecting to GitLab")
        self.conn = gitlab.Gitlab(url, apikey)
        self.conn.auth()
        logger.info("Connected to GitLab as %s",
                    self.conn.user.username)

    def run(self, out_format):
        """main entry point"""
        logger.debug("Getting users...")
        result = self.conn.User()
        logger.debug("Got users")
        logger.info("Found %d users", len(result))
        users = {}
        for user in result:
            users[user.id] = user.email

        if out_format == 'json':
            print(json.dumps(users, sort_keys=True, indent=4))
            return

        if out_format == 'csv':
            print(', '.join(sorted(users.values())))
            return

        for u in sorted(users.values()):
            print(u)


def parse_args(argv):
    """
    parse arguments/options

    this uses the new argparse module instead of optparse
    see: <https://docs.python.org/2/library/argparse.html>
    """
    p = argparse.ArgumentParser(description='Dump list of GitLab user emails ')
    p.add_argument('-v', '--verbose', dest='verbose', action='store_true',
                   default=False,
                   help='verbose output')
    p.add_argument('-f', '--format', dest='out_format', action='store', type=str,
                   default='list', choices=['list', 'csv', 'json'],
                   help="output format; one of: 'list' (one email per line), "
                   "'json' (JSON of user ID to email), 'csv' (CSV email addresses)")
    p.add_argument('gitlab_url', action='store',
                   help='URL to GitLab instance')

    args = p.parse_args(argv)

    return args

def get_api_key():
    if 'GITLAB_TOKEN' in os.environ:
        return os.environ['GITLAB_TOKEN']
    return raw_input("Enter your GitLab Private API token: ")

if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    syncer = GitLabEmailList(args.gitlab_url, get_api_key())
    syncer.run(args.out_format)
