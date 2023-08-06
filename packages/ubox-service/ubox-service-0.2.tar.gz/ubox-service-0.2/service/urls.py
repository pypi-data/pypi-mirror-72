from django.conf.urls import url
from service import views

urlpatterns = [
    url('endpoint', views.endpoint),
]
