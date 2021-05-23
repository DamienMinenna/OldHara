from . import views
from django.urls import path

urlpatterns = [
    path('', views.view_home, name='home'),
    path('/modify_biblio', views.modify_biblio, name='modify_biblio')
]
