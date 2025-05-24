from django.urls import path
from . import views

urlpatterns = [
    path("author_analytics", views.author_analytics,  name="author_analytics"),
    path("cientific_prod", views.cientific_prod,  name="cientific_prod")
]