# coding: utf-8

import os
from fabkit import run, sudo, filer, Package, expect, api
from oslo_config import cfg

CONF = cfg.CONF


tmp_dest = os.path.join(CONF._remote_tmp_dir, 'git')


def setup():
    Package('git').install()
    Package('expect').install()
    filer.mkdir(tmp_dest, mode='777')


def sync(url, branch='master', dest=None, user=None):
    if not dest:
        name = url.rsplit('/', 1)[1]
        dest = os.path.join(tmp_dest, name)

    if not filer.exists(dest):
        with api.cd('/tmp'):
            expect('git clone -b {0} {1} {2}'.format(branch, url, dest),
                   expects=[
                   ['Are you sure you want to continue connecting (yes/no)?', 'yes\\n'],
                   ],
                   user=user)
    else:
        if user is not None:
            sudo('cd {0} && git pull'.format(dest), user=user)
        else:
            run('cd {0} && git pull'.format(dest))

    return dest
