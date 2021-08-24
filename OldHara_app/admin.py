from django.contrib import admin
from .models import Biblio, Path_Biblio

# Register your models here.


class BiblioAdmin(admin.ModelAdmin):
    list_display = ('title', 'status','created_on')
    list_filter = ("status",)
    search_fields = ['title', 'abstract']

admin.site.register(Biblio, BiblioAdmin)


class Path_BiblioAdmin(admin.ModelAdmin):
    list_display = ('path',)
    search_fields = ['path']

admin.site.register(Path_Biblio, Path_BiblioAdmin)
