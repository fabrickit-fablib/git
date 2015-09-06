# coding: utf-8

import os
from fabkit import run, filer, Package, conf


tmp_git_dir = os.path.join(conf.REMOTE_TMP_DIR, 'git')


def setup():
    Package('git').install()
    filer.mkdir(tmp_git_dir, mode='777')


def sync(git_url, name=None, git_dir=None):
    if git_dir:
        git_base_dir = git_dir.rsplit('/', 1)[0]
        filer.mkdir(git_base_dir, mode='777')
    else:
        name = git_url.split(' ')[0].rsplit('/', 1)[1]
        git_dir = os.path.join(git_dir, name)

    if not filer.exists(git_dir):
        run('git clone {0} {1}'.format(git_url, git_dir))
    else:
        run('cd {0} && git pull'.format(git_dir))

    return git_dir
