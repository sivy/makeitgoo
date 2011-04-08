import os, site

os.environ['DJANGO_SETTINGS_MODULE'] = 'makeitgoo.settings'

site.addsitedir('/var/makeitgoo/makeitgoo/virtual/lib/python2.6/site-packages')
site.addsitedir(os.path.realpath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
site.addsitedir(os.path.realpath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + '/makeitgoo' ))

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
