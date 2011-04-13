# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Deploy.message'
        db.add_column('mgapp_deploy', 'message', self.gf('django.db.models.fields.CharField')(default='', max_length=512, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Deploy.message'
        db.delete_column('mgapp_deploy', 'message')


    models = {
        'mgapp.app': {
            'Meta': {'object_name': 'App'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'remote_head': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'remote_url': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['sites.Site']", 'unique': 'True'}),
            'wd': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'})
        },
        'mgapp.deploy': {
            'Meta': {'object_name': 'Deploy'},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'deployments'", 'to': "orm['mgapp.App']"}),
            'complete': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            'output': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['mgapp']
