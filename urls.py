from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

import nexus

# sets up the default nexus site by detecting all nexus_modules.py files
nexus.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^makegoo/', include('makegoo.foo.urls')),
    ('^', include('mgapp.urls')),
    
    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    (r'^nexus/', include(nexus.site.urls)),
)
