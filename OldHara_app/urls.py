from . import views
from django.urls import path

urlpatterns = [
    path('', views.view_home, name='home'),
    path(r'^ajax/modify_volume/$', views.modify_volume, name='modify_volume')
]
