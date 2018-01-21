from django.contrib import admin

from examples.models import Example


class ExampleAdmin(admin.ModelAdmin):

    list_display = ['pk', 'description']

admin.site.register(Example, ExampleAdmin)
