gitlab-scripts
==============

Some Python scripts to help administering and migrating to GitLab.

Note that per [Issue #63](https://github.com/gpocentek/python-gitlab/issues/63) there's a bug
in the current (0.9.2) version of python-gitlab that prevents retrieving more than 20 results
for ANY query.

Contents
--------

* __gitlab_email_list.py__ - Print a list of all GitLab user emails, one-per line, CSV or JSON
* __gitlab_repo_import.py__ - Helper to import an existing bare git repo into GitLab and set options/features and group ownership.
* __gitlab_ssh_key_sync.py__ - Script to sync your ~/.ssh/authorized_keys to a GitLab instance.

Usage
------

1. ``pip install python-gitlab`` (tested weith 0.9.2)
2. Use the scripts.

License
-------

gitlab-scripts is licensed under the GNU GPL v3.

Contributions back are greatly appreciated.
