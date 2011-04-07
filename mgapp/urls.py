import os.path
from django.conf.urls.defaults import *

app_path = os.path.dirname(__file__)
media_dir = os.path.join(app_path, 'static')

urlpatterns = patterns('mgapp.views',
    url(r'^$', 'home', name='home'),
    url(r'^app/(?P<app_id>[\d]+)$', 'app', name='app'),
    url(r'^save_git/(?P<app_id>[\d]+)$', 'save_git', name='save_git'),
    url(r'^deploy/(?P<deploy_id>[\d]+)$', 'deploy', name='deploy'),
    # deploy
    url(r'^deploy_app$', 'deploy_app', name='deploy_app'),
    url(r'^deploys$', 'deploys', name='deploys'),
)

urlpatterns += patterns('',
    url(r'^static/(?P<path>.*)/?$', 'django.views.static.serve', 
        name="static",
        kwargs={ 'document_root': media_dir }),
)
