from django.contrib import admin
import django.utils.safestring

from models import App, Deploy

class AppManager(admin.ModelAdmin):
    fieldsets = (
            (None, {
                'fields': ('user', 'name', 'wd')
            }),
            ('Git options', {
                'fields': ('remote_url', 'remote_head')
            }),
        )

class DeployManager(admin.ModelAdmin):
    list_display = ['app', 'created', 'complete']

admin.site.register(Deploy, DeployManager)
admin.site.register(App, AppManager)