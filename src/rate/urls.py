from django.urls import path

from rate import views


app_name = 'rate'

urlpatterns = [
    path('list/', views.RateListView.as_view(), name='list'),
]
