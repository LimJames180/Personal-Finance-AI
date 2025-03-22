from django.db.models import Sum
from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Transaction
from .forms import TransactionForm
# Create your views here.

@login_required
def home(request):
    total_spending = float(Transaction.objects.filter(user=request.user, transaction_type='expense').aggregate(total_spending=Sum('amount'))['total_spending'] or 0.00)
    total_earnings = float(Transaction.objects.filter(user=request.user, transaction_type='income').aggregate(total_earnings=Sum('amount'))['total_earnings'] or 0.00)
    budget_left = total_earnings - total_spending

    # Fetch data for the charts
    spending_data = list(Transaction.objects.filter(user=request.user, transaction_type='expense').values_list('amount', flat=True))
    earnings_data = list(Transaction.objects.filter(user=request.user, transaction_type='income').values_list('amount', flat=True))

    context = {
        'total_spending': total_spending,
        'total_earnings': total_earnings,
        'budget_left': budget_left,
        'spending_data': spending_data,
        'earnings_data': earnings_data,
    }
    return render(request, 'tracker/home.html', context)


@login_required
def transaction_history(request):
    transactions = Transaction.objects.filter(user=request.user).order_by("-date")

    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect("transaction_history")
    else:
        form = TransactionForm()

    return render(request, "tracker/transaction_history.html", {"transactions": transactions, "form": form})
