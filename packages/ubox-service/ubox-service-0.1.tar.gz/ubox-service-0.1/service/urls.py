from django.urls import path
from service import views

urlpatterns = [
    path('endpoint', views.endpoint),
]
