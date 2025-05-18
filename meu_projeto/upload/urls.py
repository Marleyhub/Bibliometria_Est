from django.urls import path
from . import views

urlpatterns = [
    path("home", views.index, name="index"),
    path("upload", views.upload, name="upload"),
    path("upload_this", views.upload_this,  name='upload_this')
]