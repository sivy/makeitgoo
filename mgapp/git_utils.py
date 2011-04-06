from __future__ import with_statement
from fabric.api import *

def _run(cmd, wd=None, local=True):
    if not wd:
        wd = "."
    with cd(wd):
        if local:
            return local(cmd, capture=True)
        else:
            return run(cwd, capture=True)

def current_commit(wd=None, local=True):
    cmd = 'git log -n1 --pretty="%H"'
    return _run(cmd, wd, local=local)

# ---

def checkout(wd=None, local=True):
    cmd = 'git checkout'
    return _run(cmd, wd=wd, local=local)
    
def branch(wd=None, local=True):
    cmd = 'git rev-parse --symbolic-full-name --abbrev-ref HEAD'
    return _run(cmd, wd=wd, local=local)

def set_remote(wd=None, local=True):
    cmd = 'git remote set-url origin'
    return _run(cmd, wd=wd, local=local)

def status(wd=None, local=True):
    cmd = 'git status'
    return _run(cmd, wd=wd, local=local)

def merge_base(wd=None, local=True):
    cmd = 'git merge-base'
    return _run(cmd, wd=wd, local=local)

def upstream(wd=None, local=True):
    cmd = 'git rev-parse @{u}'
    return _run(cmd, wd=wd, local=local)

def head(wd=None, local=True):
    cmd = 'git rev-parse HEAD'
    return _run(cmd, wd=wd, local=local)

def remote_url(wd=None, local=True):
    cmd = 'git config --get remote.origin.url'
    return _run(cmd, wd=wd, local=local)
