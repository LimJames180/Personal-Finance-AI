from django.urls import path
from . import views
from .views import home, transaction_history, summary, settings,debt_history

urlpatterns = [
    path("home/", home, name="tracker_home"),  # URL for Dashboard (Home)
    path("transactions/", transaction_history, name="transaction_history"),  # URL for Transactions
    path("summary/", summary, name="summary"),  # URL for Summary
    path("settings/", settings, name="settings"),  # URL for Settings
    path('analyze-text/', views.analyze_text, name='analyze_text'),

    path("debts/", debt_history, name="debt_history")
]