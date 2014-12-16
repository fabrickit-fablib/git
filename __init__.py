# coding: utf-8

import os
from lib.api import run, filer, package
from lib import conf


git_dir = os.path.join(conf.REMOTE_TMP_DIR, 'git')


def setup():
    package.install('git')
    filer.mkdir(git_dir, mode='777')


def sync(git_url, name=None):
    if not name:
        name = git_url.split(' ')[0].rsplit('/', 1)[1]

    clone_dir = os.path.join(git_dir, name)
    if not filer.exists(clone_dir):
        run('git clone {0} {1}'.format(git_url, clone_dir))
    else:
        run('cd {0} && git pull'.format(clone_dir))

    return clone_dir
