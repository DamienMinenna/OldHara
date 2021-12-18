from . import views
from django.urls import path

"""
OldHara urls.
"""

urlpatterns = [
    path('', views.view_home, name='home'),
    path('update_ref', views.update_ref, name='update_ref'),
    path('ref/<int:num>/', views.view_ref, name='view_ref'),
]
