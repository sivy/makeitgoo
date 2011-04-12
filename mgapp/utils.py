from fabric.api import *

import sys, subprocess, shlex, traceback, os

def _escape_shell_command(command):
    for n in ('`', '$', '"'):
        command = command.replace(n, '\%s' % n)
    return command

def run_cmd(cmd, wd=None, runlocal=False, echo=False, shell=False):
    if wd==None:
        wd='.'
    prefix=''
    if echo:
        prefix = "> %s\n" % cmd
    
    if shell:
        cmd = _escape_shell_command(cmd)

    if runlocal:
        with lcd(wd):
            return prefix + local(cmd, capture=True)
    else:
        with cd(wd):
            return prefix + run(cmd, shell=shell)