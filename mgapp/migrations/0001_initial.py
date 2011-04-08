# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'App'
        db.create_table('mgapp_app', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['sites.Site'], unique=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('mgapp', ['App'])

        # Adding model 'Deploy'
        db.create_table('mgapp_deploy', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('app', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mgapp.App'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('deploy_id', self.gf('django.db.models.fields.TextField')()),
            ('complete', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('output', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('mgapp', ['Deploy'])


    def backwards(self, orm):
        
        # Deleting model 'App'
        db.delete_table('mgapp_app')

        # Deleting model 'Deploy'
        db.delete_table('mgapp_deploy')


    models = {
        'mgapp.app': {
            'Meta': {'object_name': 'App'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'site': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['sites.Site']", 'unique': 'True'})
        },
        'mgapp.deploy': {
            'Meta': {'object_name': 'Deploy'},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mgapp.App']"}),
            'complete': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'deploy_id': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
