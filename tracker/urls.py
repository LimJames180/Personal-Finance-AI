from django.urls import path
from .views import home

urlpatterns = [
    path("home/", home, name="tracker_home"),  # URL pattern for home
]
