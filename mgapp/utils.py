from __future__ import with_statement
from fabric.api import *

def run_cmd(cmd, wd=None, runlocal=True):
    if wd is None:
        wd = "."
    cmd = "cd %s; %s" % (wd, cmd)
    if runlocal:
        return local(cmd, capture=True)
    else:
        return run(cwd, capture=True)
