from django.urls import path
from . import views

urlpatterns = [
    path("index", views.index, name="index"),
    path("analytics", views.index, name="analytics"),
    path("analyse_this", views.analyse_this,  name="analyse_this")
]