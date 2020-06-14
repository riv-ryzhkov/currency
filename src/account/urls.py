from account import views

from django.urls import path

app_name = 'account'

urlpatterns = [
    path('smoke/', views.smoke, name='smoke'),
]