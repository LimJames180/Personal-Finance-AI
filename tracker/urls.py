from django.urls import path
from .views import home, transaction_history, summary, settings

urlpatterns = [
    path("home/", home, name="tracker_home"),  # URL for Dashboard (Home)
    path("transactions/", transaction_history, name="transaction_history"),  # URL for Transactions
    path("summary/", summary, name="summary"),  # URL for Summary
    path("settings/", settings, name="settings"),  # URL for Settings
]