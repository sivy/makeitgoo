from __future__ import with_statement
from fabric.api import *

import sys, subprocess, shlex, traceback, os

def _escape_shell_command(command):
    for n in ('`', '$', '"'):
        command = command.replace(n, '\%s' % n)
    return command

def run_cmd(cmd, wd=None, runlocal=True, echo=False, shell=False):
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
            return prefix + run(cwd, capture=True, shell=shell)

def _run_cmd(cmd, wd=None, runlocal=True, echo=False, shell=False):
    out = ''
    if wd!=None:
        if echo:
            out += 'cd ' + wd + "\n"
        os.chdir(wd)

    prefix=''
    if echo:
        out += "> %s\n" % cmd    

    if shell:
        cmd = _escape_shell_command(cmd)
    else:
        cmd = shlex.split(cmd.encode('ascii'))

    stdout_str, stderr_str = '',''
    
    try:
        proc = subprocess.Popen(cmd,
                                shell=shell,
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
    
    return out + "\n" + stdout_str.rstrip() + stderr_str.rstrip()
