from django.urls import path
from .views import home,transaction_history

urlpatterns = [
    path("home/", home, name="tracker_home"),  # URL pattern for home
    path("transactions/", transaction_history, name="transaction_history"),

]

