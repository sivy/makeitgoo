from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

import nexus

# sets up the default nexus site by detecting all nexus_modules.py files
nexus.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^makeitgoo/', include('makeitgoo.foo.urls')),
    (r'^', include('mgapp.urls')),
    
    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    (r'^nexus/', include(nexus.site.urls)),
)
