from django.urls import path
from . import views

urlpatterns = [
    path("author_analytics", views.author_analytics,  name="author_analytics"),
]