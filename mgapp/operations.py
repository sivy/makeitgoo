from utils import run_cmd
import git_utils as git
import sys, os

def save_git(wd, remote=None, branch=None):
    output = ''
    if (remote):
        output += git.set_remote(git_remote, wd=wd)
    if (branch):
        output += git.checkout(git_branch, wd=wd)
    return output

def update_env(wd):
    # env is in ./virtual
    # requirements are in ./requirements.txt
    output = run_cmd('source virtual/bin/activate', wd=wd, echo=True)
    output += run_cmd('pip install -r requirements.txt', wd=wd, echo=True)
    return output