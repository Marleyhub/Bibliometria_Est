from django.urls import path
from . import views

urlpatterns = [
    path("analyse_this", views.analyse_this,  name="analyse_this"),
]