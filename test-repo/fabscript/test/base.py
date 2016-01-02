# coding: utf-8

from fabkit import task, sudo
from fablib import git


@task
def setup():
    git.setup()
    sudo('rm -rf /tmp/git')
    git.sync('https://github.com/fabrickit-fablib/git.git')
    git.sync('https://github.com/fabrickit-fablib/git.git', dest='/tmp/git')
    git.sync('https://github.com/fabrickit-fablib/git.git', dest='/tmp/git')
