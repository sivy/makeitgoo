import subprocess, shlex

def _run(cmd):
    cmd = shlex.split(cmd)
    return subprocess.Popen(cmds, stdout=subprocess.PIPE).communicate()[0]

def current_commitish():
    cmd = 'git log -n1 --pretty="%H"'
    return _run(cmd)

