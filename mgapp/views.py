from __future__ import with_statement
import time
from urlparse import urlsplit
from urllib import unquote_plus

from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseServerError
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from django.contrib.csrf.middleware import csrf_exempt
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

from mgapp.models import App, Deploy

def _update(caption, content):
    return "%s\n----------\n%s\n\n" % (caption.upper(), content)

def _config():
    import yaml
    f = open(dsettings.SITE_CONFIG)
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
    
    deploys = Deploy.objects.filter(app=app).order_by('-created')[:5]
    
    return render_to_response("app.html", {
        'app': app,
        'deploys': deploys
    })

def deploy(request, deploy_id=None):
    
    deploy = Deploy.objects.get(id=deploy_id)
    
    return render_to_response("deploy.html", {
        'deploy': deploy
    })

@jsonp
def deploys(request):
    app_id = request.GET.get('app_id')
    app = App.objects.get(id=app_id)
    
    deploys = Deploy.objects.filter(app=app)[:5]
    return render_to_response("deploys.html", {
        'deploys': deploys
    })
    
@recordstats('')
@jsonp
def deploy_app(request):
    app_id = request.GET.get('app_id')
    app = App.objects.get(id=app_id)
    site_name = app.site.name
    
    config = _config()
    
    site_config = config['sites'][site_name]
    out = ''
    for host, config in site_config['hosts'].iteritems():
        Random.atfork()
        env.user = dsettings.SSH_USER
        env.password = config['pwd']
        env.key_filename = dsettings.SSH_KEYFILE
        env.host_string = host
        
        with cd(config['remote_root']):
            try:
                out += _update('starting in', run('pwd'))
                out += _update('update from repo', run('git pull origin master'))
                out += _update("post_update hooks", run ('sh post_update.sh'))
                out += _update('deploy built site', sudo ('cp -R _site/* %s' % config['remote_dest']))
            except Exception, e:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                formatted_lines = traceback.format_exc().splitlines()
                
                return HttpResponse("<pre>%s\nERROR: %s</pre>" % (out, formatted_lines))
    do = Deploy.objects.create(app=app, deploy_id='placeholder', output=out, complete=True)
    do.save()
    
    return HttpResponse("<pre>%s\nDEPLOYED: <a href='%s'>%s</a></pre>" % (out, site_config['url'], site_config['url']))