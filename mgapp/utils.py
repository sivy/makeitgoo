from __future__ import with_statement
from fabric.api import *

import sys, subprocess, shlex, traceback, os

def _escape_shell_command(command):
    for n in ('`', '$', '"'):
        command = command.replace(n, '\%s' % n)
    return command

def _run_cmd(cmd, wd=None, runlocal=True, echo=False):
    if wd==None:
        wd='.'
    prefix=''
    cmd = _escape_shell_command(cmd)
    if echo:
        prefix = "> %s\n" % cmd
    if runlocal:
        with lcd(wd):
            return prefix + local(cmd, capture=True)
    else:
        with cd(wd):
            return prefix + run(cwd, capture=True)

def run_cmd(cmd, wd=None, runlocal=True, echo=False):
    if wd!=None:
        os.chdir(wd)


    prefix=''
    cmd = shlex.split(cmd.encode('ascii'))

    out, stdout_str, stderr_str = '','',''
    if echo:
        out = "> %s\n" % cmd    
    
    try:
        proc = subprocess.Popen(cmd,
                                stdout = subprocess.PIPE,
                                stderr = subprocess.PIPE)

        stdout_str, stderr_str = proc.communicate()
        print stdout_str, stderr_str
        if proc.returncode:
            stderr_str += "\n\n*** Process ended with return code %d\n\n" % proc.returncode

    except Exception, e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        formatted_lines = traceback.format_exc().splitlines()
        stderr_str += unicode(e) + '\n'.join(formatted_lines)
    
    return stdout_str.rstrip() + stderr_str.rstrip()