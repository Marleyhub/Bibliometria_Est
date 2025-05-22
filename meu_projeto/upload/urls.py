from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload, name="upload"),
    path("upload_this", views.upload_this,  name="upload_this")
]