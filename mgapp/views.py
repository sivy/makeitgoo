import time
from urlparse import urlsplit
from urllib import unquote_plus

from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseServerError
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.template.loader import render_to_string
from django.contrib.csrf.middleware import csrf_exempt
from django.core.context_processors import csrf
from django.core import serializers
from django.db.models import Sum
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

import simplejson as json

import logging

import stats_util as stats

from decorators import jsonp, recordstats

from fabric.api import *

from django.conf import settings as dsettings
from Crypto import Random

import sys, traceback
import git_utils as git
from utils import run_cmd

from mgapp.models import App, Deploy
import operations

from fabric.api import *

GIT = dsettings.GIT

def _update(caption, content):
    return "%s\n----------\n%s\n\n" % (caption.upper(), content)


def _get_config(wd):
    import yaml
    f = open("%s/mig.yaml" % wd)
    config = yaml.load(f)
    f.close()
    return config


## http://en.gravatar.com/site/implement/images/python/

@login_required
def home(request):    
    apps = App.objects.filter(user=request.user)
    for app in apps:
        app.load_config()
    
    deploys = Deploy.objects.filter(app__user=request.user).order_by('-created')[:30]
    return render_to_response("home.html", {
        'apps': apps,
        'deploys': deploys
    }, context_instance=RequestContext(request))


@login_required
def app(request, app_id=None):
    app = App.objects.get(id=app_id)
    app.load_config()
        
    envs = []
    
    if ("envs" in app.config):
        for label, env_data in app.config['envs'].iteritems():
            env_data['label'] = label
            
            env.host_string = env_data['host']
            host = env_data['host']
            if '@' in host:
                host = host.split('@')[1]
            env.key_filename = dsettings.SSH_KEY_DIR + '/deploy_rsa'
            env.no_keys = True
            env.user = 'deploy'
                        
            print env
            
            with cd(env_data['working_dir']):
                print run('pwd')
                git_info = {
                    'head': git.head().rstrip(),
                    'remote': git.remote_url().rstrip(),
                    'branch': git.branch().rstrip(),
                }
                env_data['git'] = git_info
            
            envs.append(env_data)
    
    deploys = Deploy.objects.filter(app=app).order_by('-created')[:5]
    
    c = {
        'app': app,
        'envs': envs,
        'git': {},
        'deploys': deploys,
    }
    c.update(csrf(request))
    
    return render_to_response("app.html", c, context_instance=RequestContext(request))


@login_required
def create_app(request):
    user = request.user
    name = request.POST.get('name')
    remote = request.POST.get('remote')

    app = App.objects.create(name=name, remote_url=remote, user=user)
    
    appserver_root = dsettings.APPSERVER_ROOT
    wd = '%s/%s' % (appserver_root, name)
    res = local('mkdir -p %s' % wd)
    if res.return_code == 0:
        local('chmod 777 %s' % wd)
        app.wd = wd
    else:
        return HttpResponseServerError('could not setup working directory')

    app.save()

    with lcd(app.wd):
        with settings(warnings_only=True):
            print local('pwd', capture=True)
            cmd = GIT + ' clone %s .' % remote
            print "CLONE: " + local(cmd, capture=True)
    
    return redirect ( 'mgapp.views.app', app_id=app.id )

@login_required
def save_git(request, app_id=None):
    app = App.objects.get(id=app_id)
    
    git_remote = request.POST.get('remote')
    git_branch = request.POST.get('branch')
    
    if not (git_remote and git_branch):
        return HttpResponseServerError("no remote or branch")
    
    output = operations.save_git(remote=git_remote, branch=git_branch)
    
    return HttpResponse (output)


@login_required
def deploy(request, deploy_id=None):
    
    deploy = Deploy.objects.get(id=deploy_id)
    
    return render_to_response("deploy.html", {
        'deploy': deploy
    }, context_instance=RequestContext(request))


@jsonp
def deploys(request):
    app_id = request.GET.get('app_id')
    count = request.GET.get('count')
    partial = request.GET.get('partial')
    if partial:
        t = "deploy_list.html"
    else:
        t = "deploys.html"
    
    app = App.objects.get(id=app_id)
    
    deploys = Deploy.objects.filter(app=app).order_by('-created')[:count]
    return render_to_response(t, {
        'app': app,
        'deploys': deploys
    }, context_instance=RequestContext(request))


@recordstats('')
@jsonp
def deploy_app(request):
    app_id = request.GET.get('app_id')
    message = request.GET.get('message')
    env_label = request.GET.get('env')
    
    app = App.objects.get(id=app_id)
    app.load_config()

    site_name = app.name
    wd = app.wd

    do = Deploy.objects.create(message=message, app=app)
    
    if not "envs" in app.config:
        return HttpResponseServerError("no deploy environments defined for app " + app.name)
    
    config = app.config
    print config

    out = ''

    if (config['type'] == 'static'):
        if 'envs' in config:
            if env_label in config['envs']:
                Random.atfork()
                env_data = config['envs'][env_label]
                print env_data
                
                env.host_string = env_data['host']
                host = env_data['host']
                if '@' in host:
                    host = host.split('@')[1]
                env.key_filename = dsettings.SSH_KEY_DIR + '/deploy_rsa'
                env.no_keys = True
                env.user = 'deploy'                
                
                try:
                    with settings(warn_only=True):
                        if run("test -d %s" % env_data['working_dir']).failed:
                            run('mkdir -p %s' % env_data['working_dir'])
                        with cd(env_data['working_dir']):
                            with hide('running', 'stderr', 'stdout', 'output', 'aborts', 'warnings', 'status', 'user'):                        
                                res = run('pwd')
                                if res.failed:
                                    do.out=out
                                    do.complete=False
                                    do.save()
                                    return HttpResponseServerError(
                                        "<pre>ERROR:\n\n%s</pre>" % res)
                                out += _update("starting in", res)
                                
                                res = git.update()
                                if res.failed:
                                    do.out=out
                                    do.complete=False
                                    do.save()
                                    return HttpResponseServerError(
                                        "<pre>ERROR:\n\n%s</pre>" % res)
                                out += _update("update from repo", res)
                                
                                if 'post_update' in env_data:
                                    res = run('sh %' % env_data['post_update'])
                                    if res.failed:
                                        do.out=out
                                        do.complete=False
                                        do.save()
                                        return HttpResponseServerError(
                                            "<pre>ERROR:\n\n%s</pre>" % res)
                                    out += _update("post_update hooks", res)
                                
                                res = run('cp -R %s/* %s' % (
                                    env_data['build_dir'], env_data['dest_dir']
                                    ))
                                if res.failed:
                                    do.out=out
                                    do.complete=False
                                    do.save()
                                    return HttpResponseServerError(
                                        "<pre>ERROR:\n\n%s</pre>" % res)
                                out += _update("deploy built site", res)
                                    
                except Exception, e:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    formatted_lines = traceback.format_exc().splitlines()

                    return HttpResponseServerError("<pre>%s\nERROR: %s\n\n%s</pre>" % (out, exc_value, "\n".join(formatted_lines)))
        else:
            pass
            
    if (config['type'] == 'wsgi'):
        pass
    
    do.out = out
    do.complete=True
    do.save()
    
    return HttpResponse("<pre>%s\nDEPLOYED: <a href='%s'>%s</a></pre>" % (out, config['url'], config['url']))
