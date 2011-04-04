import os.path
from django.conf.urls.defaults import *

app_path = os.path.dirname(__file__)
media_dir = os.path.join(app_path, 'static')

urlpatterns = patterns('mgapp.views',
    url(r'^$', 'home', name='home'),
    url(r'^app$', 'app', name='app'),
    # deploy
    url(r'^deploy$', 'deploy', name='deploy'),
    url(r'^deploys$', 'deploys', name='deploys'),
)
