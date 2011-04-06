from __future__ import with_statement
from fabric.api import *

def _run(cmd, wd=None, runlocal=True):
    if not wd:
        wd = "."
    with cd(wd):
        if runlocal:
            return local(cmd, capture=True)
        else:
            return run(cwd, capture=True)

def current_commit(wd=None, runlocal=True):
    cmd = 'git log -n1 --pretty="%H"'
    return _run(cmd, wd=wd, runlocal=runlocal)

# ---

def checkout(commitish, wd=None, runlocal=True):
    cmd = 'git checkout %s' % commitish
    return _run(cmd, wd=wd, runlocal=runlocal)
    
def branch(wd=None, runlocal=True):
    cmd = 'git rev-parse --symbolic-full-name --abbrev-ref HEAD'
    return _run(cmd, wd=wd, runlocal=runlocal)

def set_remote(remote, wd=None, runlocal=True):
    cmd = 'git remote set-url origin %s' % remote
    return _run(cmd, wd=wd, runlocal=runlocal)

def status(wd=None, runlocal=True):
    cmd = 'git status'
    return _run(cmd, wd=wd, runlocal=runlocal)

def merge_base(wd=None, runlocal=True):
    cmd = 'git merge-base'
    return _run(cmd, wd=wd, runlocal=runlocal)

# apparently b0rken
def upstream(wd=None, runlocal=True):
    cmd = 'git rev-parse @{u}'
    return _run(cmd, wd=wd, runlocal=runlocal)

def head(wd=None, runlocal=True):
    cmd = 'git rev-parse HEAD'
    return _run(cmd, wd=wd, runlocal=runlocal)

def remote_url(wd=None, runlocal=True):
    cmd = 'git config --get remote.origin.url'
    return _run(cmd, wd=wd, runlocal=runlocal)
