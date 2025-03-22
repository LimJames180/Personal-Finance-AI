from django.urls import path
from . import views
from .views import home, transaction_history, advisor, settings,debt_history,delete_debt,delete_transaction

urlpatterns = [
    path("home/", home, name="tracker_home"),  # URL for Dashboard (Home)
    path("transactions/", transaction_history, name="transaction_history"),  # URL for Transactions
    path("advisor/", advisor, name="advisor"),  # URL for Summary
    path("settings/", settings, name="settings"),  # URL for Settings
    path('analyze-text/', views.analyze_text, name='analyze_text'),

    path("debts/", debt_history, name="debt_history"),
    path('delete-debt/<int:debt_id>/', delete_debt, name='delete_debt'),
    path('delete-transaction/<int:transaction_id>/', delete_transaction, name='delete_transaction'),



]