from django.urls import path

from . import views


app_name = 'User'

urlpatterns = [
    path('create', views.createUser, name='create'),
    path('auth', views.login, name='auth'),
    path('refresh', views.refresh, name='refresh')
]
