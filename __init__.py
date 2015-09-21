# coding: utf-8

import os
from fabkit import sudo, filer, Package, conf, expect


tmp_git_dir = os.path.join(conf.REMOTE_TMP_DIR, 'git')


def setup():
    Package('git').install()
    Package('expect').install()
    filer.mkdir(tmp_git_dir, mode='777')


def sync(url, branch='master', git_dir=None, owner='root:root'):
    if git_dir:
        git_base_dir = git_dir.rsplit('/', 1)[0]
        filer.mkdir(git_base_dir)
    else:
        name = url.rsplit('/', 1)[1]
        git_dir = os.path.join(tmp_git_dir, name)

    if not filer.exists(git_dir):
        expect('git clone -b {0} {1} {2}'.format(branch, url, git_dir),
               expects=[
               ['Are you sure you want to continue connecting (yes/no)?', 'yes\\n'],
               ],
               use_sudo=True)
        sudo('chown -R {0} {1}'.format(owner, git_dir))
    else:
        sudo('cd {0} && git pull'.format(git_dir))

    return git_dir
