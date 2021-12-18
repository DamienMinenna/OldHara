from django.contrib import admin

from .models import Ref, Folder_Refs

"""
Models registered for the admin panel.
"""


class RefAdmin(admin.ModelAdmin):
    list_display = ('title', 'status','created_on')
    list_filter = ("status",)
    search_fields = ['title', 'abstract']

admin.site.register(Ref, RefAdmin)


class Folder_RefAdmin(admin.ModelAdmin):
    list_display = ('path',)
    search_fields = ['path']

admin.site.register(Folder_Refs, Folder_RefAdmin)

