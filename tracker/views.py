from datetime import datetime, timedelta

from django.db.models import Sum
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Transaction
from .forms import TransactionForm


# Home view
@login_required
def home(request):
    total_spending = float(Transaction.objects.filter(user=request.user, transaction_type='expense').aggregate(
        total_spending=Sum('amount'))['total_spending'] or 0.00)
    total_earnings = float(Transaction.objects.filter(user=request.user, transaction_type='income').aggregate(
        total_earnings=Sum('amount'))['total_earnings'] or 0.00)
    budget_left = total_earnings - total_spending

    # Fetch data for the charts
    spending_data = list(
        Transaction.objects.filter(user=request.user, transaction_type='expense').values_list('amount', flat=True))
    earnings_data = list(
        Transaction.objects.filter(user=request.user, transaction_type='income').values_list('amount', flat=True))

    context = {
        'total_spending': total_spending,
        'total_earnings': total_earnings,
        'budget_left': budget_left,
        'spending_data': spending_data,
        'earnings_data': earnings_data,
    }
    return render(request, 'tracker/home.html', context)


# Transaction history view
@login_required
def transaction_history(request):
    current_date = datetime.now()
    start_date = current_date - timedelta(days=30)

    total_expenses = float(Transaction.objects.filter(
        user=request.user,
        transaction_type='expense',
        date__range=[start_date, current_date]
    ).aggregate(total_expenses=Sum('amount'))['total_expenses'] or 0.00)

    total_income = float(Transaction.objects.filter(
        user=request.user,
        transaction_type='income',
        date__range=[start_date, current_date]
    ).aggregate(total_income=Sum('amount'))['total_income'] or 0.00)

    net_balance = total_income - total_expenses

    recent_transactions = Transaction.objects.filter(
        user=request.user,
        date__range=[start_date, current_date]
    ).order_by("-date")

    past_transactions = Transaction.objects.filter(
        user=request.user,
        date__lt=start_date
    ).order_by("-date")

    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect("transaction_history")
    else:
        form = TransactionForm()

    context = {
        'total_expenses': total_expenses,
        'total_income': total_income,
        'net_balance': net_balance,
        'recent_transactions': recent_transactions,
        'past_transactions': past_transactions,
        'form': form,
    }
    return render(request, "tracker/transaction_history.html", context)


# Summary view
@login_required
def summary(request):
    # Fetch all transactions for the logged-in user
    transactions = Transaction.objects.filter(user=request.user).order_by("-date")

    # Calculate total spending and earnings
    total_spending = float(Transaction.objects.filter(user=request.user, transaction_type='expense').aggregate(
        total_spending=Sum('amount'))['total_spending'] or 0.00)
    total_earnings = float(Transaction.objects.filter(user=request.user, transaction_type='income').aggregate(
        total_earnings=Sum('amount'))['total_earnings'] or 0.00)
    budget_left = total_earnings - total_spending

    context = {
        'transactions': transactions,
        'total_spending': total_spending,
        'total_earnings': total_earnings,
        'budget_left': budget_left,
    }
    return render(request, "tracker/summary.html", context)


# Settings view
@login_required
def settings(request):
    # Placeholder for settings page
    return render(request, "tracker/settings.html")


def dashboard_view(request):
    user = request.user

    # Query transactions for this user, grouped by date (or month)
    transactions = Transaction.objects.filter(user=user)

    # Prepare data for the graph (aggregated by day)
    spending_data = defaultdict(float)
    income_data = defaultdict(float)

    for transaction in transactions:
        date = transaction.date
        if transaction.transaction_type == 'expense':
            spending_data[date] += transaction.amount
        elif transaction.transaction_type == 'income':
            income_data[date] += transaction.amount

    # Prepare the data for the line graph
    dates = sorted(set(spending_data.keys()).union(set(income_data.keys())))
    expense_values = [spending_data.get(date, 0) for date in dates]
    income_values = [income_data.get(date, 0) for date in dates]

    # Format dates for the chart labels
    date_labels = [date.strftime('%b %d') for date in dates]

    context = {
        'total_spending': sum(expense_values),
        'total_earnings': sum(income_values),
        'budget_left': 1000 - sum(expense_values),  # Example: subtract spending from budget
        'expense_data': expense_values,
        'income_data': income_values,
        'months': date_labels,
    }
    return render(request, 'tracker/home.html', context)