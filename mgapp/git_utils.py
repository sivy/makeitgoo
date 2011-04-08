from __future__ import with_statement
from fabric.api import *
from django.conf import settings as dsettings

from utils import run_cmd

GIT=dsettings.GIT

def current_commit(wd=None, runlocal=True):
    cmd = GIT + ' log -n1 --pretty="%H"'
    return run_cmd(cmd, wd=wd, runlocal=runlocal)

# ---

def checkout(commitish, wd=None, runlocal=True):
    cmd = GIT + ' checkout %s' % commitish
    return run_cmd(cmd, wd=wd, runlocal=runlocal)
    
def branch(wd=None, runlocal=True):
    cmd = GIT + ' rev-parse --symbolic-full-name --abbrev-ref HEAD'
    return run_cmd(cmd, wd=wd, runlocal=runlocal)

def set_remote(remote, wd=None, runlocal=True):
    cmd = GIT + ' remote set-url origin %s' % remote
    return run_cmd(cmd, wd=wd, runlocal=runlocal)

def status(wd=None, runlocal=True):
    cmd = GIT + ' status'
    return run_cmd(cmd, wd=wd, runlocal=runlocal)

def merge_base(wd=None, runlocal=True):
    cmd = GIT + ' merge-base'
    return run_cmd(cmd, wd=wd, runlocal=runlocal)

# apparently b0rken
def upstream(wd=None, runlocal=True):
    cmd = GIT + ' rev-parse @{u}'
    return run_cmd(cmd, wd=wd, runlocal=runlocal)

def head(wd=None, runlocal=True):
    cmd = GIT + ' rev-parse HEAD'
    return run_cmd(cmd, wd=wd, runlocal=runlocal)

def remote_url(wd=None, runlocal=True):
    cmd = GIT + ' config --get remote.origin.url'
    return run_cmd(cmd, wd=wd, runlocal=runlocal)
