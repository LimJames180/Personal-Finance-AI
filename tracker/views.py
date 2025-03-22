from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Transaction
from .forms import TransactionForm

# Create your views here.
def home(request):
    return render(request, 'tracker/home.html')


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
