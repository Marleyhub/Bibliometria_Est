from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('begin_upload', views.begin_upload, name='begin_upload')
]