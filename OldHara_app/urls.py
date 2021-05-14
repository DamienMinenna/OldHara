from . import views
from django.urls import path

urlpatterns = [
    path('', views.view_home, name='home'),
    path('select_list', views.select_list, name='select_list'),
    path('addfolder', views.view_addfolder, name='addfolder'),
    path('addentry', views.view_addentry, name='addentry')
]
