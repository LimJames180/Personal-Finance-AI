from datetime import datetime, timedelta

from django.db.models import Sum
from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Transaction
from .forms import TransactionForm
# Create your views here.

@login_required
@login_required
def home(request):
    current_date = datetime.now()
    start_date = current_date - timedelta(days=30)

    total_spending = float(Transaction.objects.filter(
        user=request.user,
        transaction_type='expense',
        date__range=[start_date, current_date]
    ).aggregate(total_spending=Sum('amount'))['total_spending'] or 0.00)

    total_earnings = float(Transaction.objects.filter(
        user=request.user,
        transaction_type='income',
        date__range=[start_date, current_date]
    ).aggregate(total_earnings=Sum('amount'))['total_earnings'] or 0.00)

    budget_left = total_earnings - total_spending

    # Fetch data for the charts
    spending_data = list(Transaction.objects.filter(
        user=request.user,
        transaction_type='expense',
        date__range=[start_date, current_date]
    ).values_list('amount', flat=True))

    earnings_data = list(Transaction.objects.filter(
        user=request.user,
        transaction_type='income',
        date__range=[start_date, current_date]
    ).values_list('amount', flat=True))

    # Fetch spending categories data
    spending_categories = Transaction.objects.filter(
        user=request.user,
        transaction_type='expense',
        date__range=[start_date, current_date]
    ).values('category').annotate(total=Sum('amount')).order_by('category')

    context = {
        'total_spending': total_spending,
        'total_earnings': total_earnings,
        'budget_left': budget_left,
        'spending_data': spending_data,
        'earnings_data': earnings_data,
        'spending_categories': list(spending_categories),
    }
    return render(request, 'tracker/home.html', context)


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