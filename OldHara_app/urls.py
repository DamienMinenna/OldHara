from . import views
from django.urls import path

urlpatterns = [
    path('', views.view_home, name='home'),
    path('add_biblio', views.view_add_biblio, name='add_biblio'),
    path('/modify_biblio', views.modify_biblio, name='modify_biblio')
]
