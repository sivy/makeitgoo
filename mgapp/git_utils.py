from fabric.api import *
from django.conf import settings as dsettings

"""
These are designed to be called from a fabric context
"""

def current_commit():
    cmd = 'git log -n1 --pretty="%H"'
    return run(cmd)

# ---
def clone(remote):
    cmd = 'git clone %s' % remote
    return run(cmd)

def update():
    cmd = 'git pull origin master'
    return run(cmd)

def checkout(commitish):
    cmd = 'git checkout %s' % commitish
    return run(cmd)
    
def branch():
    cmd = 'git rev-parse --symbolic-full-name --abbrev-ref HEAD'
    return run(cmd)

def set_remote(remote):
    cmd = 'git remote set-url origin %s' % remote
    return run(cmd)

def status():
    cmd = 'git status'
    return run(cmd)

def merge_base():
    cmd = 'git merge-base'
    return run(cmd)

# apparently b0rken
def upstream():
    cmd = 'git rev-parse @{u}'
    return run(cmd)

def head():
    cmd = 'git rev-parse HEAD'
    return run(cmd)

def remote_url():
    cmd = 'git config --get remote.origin.url'
    return run(cmd)
