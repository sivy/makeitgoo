from django.db import models
from datetime import datetime
# Create your models here.

from django.contrib.sites.models import Site
import sys

import git_utils

class App(models.Model):
    site = models.OneToOneField(Site, blank=False)
    name = models.CharField(blank=False, max_length=100, verbose_name="Application Name")
    wd = models.CharField(blank=True, max_length=512, verbose_name="Working Directory")
    remote_url = models.CharField(max_length=100, blank=True)
    remote_head = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return self.name
    
    @property
    def latest_deploy(self):
        return self.deployments.order_by('-created')[0]
    
    def load_config(self):
        try:
            import yaml
            f = open("%s/mig.yaml" % self.wd)
            config = yaml.load(f)
            f.close()
            self.config = config
        except Exception, e:
            self.config = { 'error': e.message }
    
class Deploy(models.Model):
    app = models.ForeignKey(App, blank=False, related_name='deployments')
    created = models.DateTimeField(default=datetime.now)
    deploy_id = models.TextField(blank=False, null=False)
    complete = models.BooleanField(blank=True)
    output = models.TextField(blank=True)
    
    def __str__(self):
        return "%s [%s]" % (self.app.name, self.created)
    
    def clean(self):
        pass

