# coding: utf-8

import os
from fabkit import sudo, filer, Package, expect
from oslo_config import cfg

CONF = cfg.CONF


tmp_dest = os.path.join(CONF._remote_tmp_dir, 'git')


def setup():
    Package('git').install()
    Package('expect').install()
    filer.mkdir(tmp_dest, mode='777')


def sync(url, branch='master', dest=None, owner='root:root'):
    if dest:
        git_base_dir = dest.rsplit('/', 1)[0]
        filer.mkdir(git_base_dir)
    else:
        name = url.rsplit('/', 1)[1]
        dest = os.path.join(tmp_dest, name)

    if not filer.exists(dest):
        expect('git clone -b {0} {1} {2}'.format(branch, url, dest),
               expects=[
               ['Are you sure you want to continue connecting (yes/no)?', 'yes\\n'],
               ],
               use_sudo=True)
        sudo('chown -R {0} {1}'.format(owner, dest))
    else:
        sudo('cd {0} && git pull'.format(dest))
        sudo('chown -R {0} {1}'.format(owner, dest))

    return dest
