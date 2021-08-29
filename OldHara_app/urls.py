from . import views
from django.urls import path

urlpatterns = [
    path('', views.view_home, name='home'),
    path('info', views.view_info, name='info'),
    path('settings', views.view_settings, name='settings'),
    path('add_biblio', views.view_add_biblio, name='add_biblio'),
    path('check_biblio', views.view_check_biblio, name='check_biblio'),
    path('check_biblio/<int:num>/', views.view_check_biblio, name='check_biblio_select'),
    path('modify_biblio', views.modify_biblio, name='modify_biblio'),
]
