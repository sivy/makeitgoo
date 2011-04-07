from __future__ import with_statement
from fabric.api import *

def run_cmd(cmd, wd=None, runlocal=True, echo=False):
    if wd==None:
        wd='.'
    prefix=''
    if echo:
        prefix = "> %s\n" % cmd
    if runlocal:
        with lcd(wd):
            return prefix + local(cmd, capture=True)
    else:
        with cd(wd):
            return prefix + run(cwd, capture=True)
