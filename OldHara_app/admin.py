from django.contrib import admin
from .models import Biblio, Ref, Path_Ref

# Register your models here.


class RefAdmin(admin.ModelAdmin):
    list_display = ('title', 'status','type','created_on')
    list_filter = ("status",'type')
    search_fields = ['title', 'abstract']

admin.site.register(Ref, RefAdmin)


class Path_RefAdmin(admin.ModelAdmin):
    list_display = ('path',)
    search_fields = ['path']

admin.site.register(Path_Ref, Path_RefAdmin)


class BiblioAdmin(admin.ModelAdmin):
    list_display = ('title', 'status','type','created_on')
    list_filter = ("status",'type')
    search_fields = ['title', 'abstract']

admin.site.register(Biblio, BiblioAdmin)
