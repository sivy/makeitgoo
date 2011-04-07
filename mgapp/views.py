from __future__ import with_statement
import time
from urlparse import urlsplit
from urllib import unquote_plus

from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseServerError
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from django.contrib.csrf.middleware import csrf_exempt
from django.core.context_processors import csrf
from django.core import serializers
from django.db.models import Sum
from django.core.exceptions import ObjectDoesNotExist

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

def _update(caption, content):
    return "%s\n----------\n%s\n\n" % (caption.upper(), content)

def _get_config(wd):
    import yaml
    f = open("%s/mig.yaml" % wd)
    config = yaml.load(f)
    f.close()
    return config

def home(request):    
    apps = App.objects.all()
    return render_to_response("home.html", {
        'apps': apps,
        
    })

def app(request, app_id=None):

    app = App.objects.get(id=app_id)
    
    config = _get_config(app.wd)
    
    git_info = {
        'head': git.head(wd=app.wd),
        'remote': git.remote_url(wd=app.wd),
        'branch': git.branch(wd=app.wd)
    }
    
    deploys = Deploy.objects.filter(app=app).order_by('-created')[:5]
    
    c = {
        'app': app,
        'git': git_info,
        'deploys': deploys
    }
    c.update(csrf(request))
    
    return render_to_response("app.html", c)

def save_git(request, app_id=None):
    
    app = App.objects.get(id=app_id)

    git_remote = request.POST.get('remote')
    git_branch = request.POST.get('branch')

    if not (git_remote and git_branch):
        return HttpResponseServerError("no remote or branch")
    
    out = git.set_remote(git_remote, wd=app.wd)
    print out
    out += git.checkout(git_branch, wd=app.wd)
    print out
    
    return HttpResponse (out)
    
def deploy(request, deploy_id=None):
    
    deploy = Deploy.objects.get(id=deploy_id)
    
    return render_to_response("deploy.html", {
        'deploy': deploy
    })

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
    })

@recordstats('')
@jsonp
def deploy_app(request):
    app_id = request.GET.get('app_id')
    app = App.objects.get(id=app_id)
    site_name = app.site.name
    wd = app.wd
    
    config = _get_config(wd)
    print config

    out = ''

    if (config['type'] == 'static'):
        # try:
        out += _update('starting in', run_cmd('pwd', wd=wd, echo=True))
        out += _update('update from repo', run_cmd('git pull origin master', wd=wd, echo=True))
        out += _update("post_update hooks", run_cmd('sh post_update.sh', wd=wd, echo=True))
        out += _update('deploy built site', run_cmd('cp -R %s/* %s' % (
            config['build_dir'], config['dest_dir']
        ), wd=wd, echo=True))
        # except Exception, e:
        #             exc_type, exc_value, exc_traceback = sys.exc_info()
        #             formatted_lines = traceback.format_exc().splitlines()
        #                 
        #             return HttpResponseServerError("<pre>%s\nERROR: %s\n\n%s</pre>" % (out, exc_value, formatted_lines))
    
    do = Deploy.objects.create(app=app, deploy_id='placeholder', output=out, complete=True)
    do.save()
    
    return HttpResponse("<pre>%s\nDEPLOYED: <a href='%s'>%s</a></pre>" % (out, config['url'], config['url']))