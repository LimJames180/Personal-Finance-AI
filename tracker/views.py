from collections import defaultdict
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404, redirect

from django.db.models import Sum
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Transaction,Debt,Budget
from .forms import TransactionForm,DebtForm

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .aitransaction import aitransaction


from datetime import datetime, timedelta
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import TransactionForm
from decimal import Decimal


@login_required
def transaction_history(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user  # Assign the logged-in user
            transaction.save()  # Save the transaction to the database
            return redirect("transaction_history")  # Redirect to refresh the page
    else:
        form = TransactionForm()

    # Fetch and display recent transactions
    current_date = datetime.now()
    start_date = current_date - timedelta(days=30)

    # Fetch all transactions for the logged-in user in the last 30 days
    transactions = Transaction.objects.filter(
        user=request.user,
        date__range=[start_date, current_date]
    ).order_by("date")

    # Debugging: Print all transactions
    print("All Transactions (Last 30 Days):")
    for transaction in transactions:
        print(f"ID: {transaction.id}, Date: {transaction.date}, Type: {transaction.transaction_type}, Amount: {transaction.amount}, Category: {transaction.category}")

    # Initialize data structures
    daily_spending = {}
    daily_income = {}
    labels = []  # Days of the last 30 days

    # Initialize daily spending and income to 0 for each day of the last 30 days
    current_day = start_date
    while current_day <= current_date:
        day_str = current_day.strftime("%Y-%m-%d")
        daily_spending[day_str] = Decimal('0.00')
        daily_income[day_str] = Decimal('0.00')
        labels.append(current_day.strftime("%d %b"))  # Format: "01 May", "02 May", etc.
        current_day += timedelta(days=1)

    # Debugging: Print initialized daily_spending and daily_income
    print("Initialized Daily Spending (Last 30 Days):", daily_spending)
    print("Initialized Daily Income (Last 30 Days):", daily_income)

    # Populate daily spending and income
    for transaction in transactions:
        day_str = transaction.date.strftime("%Y-%m-%d")
        if transaction.transaction_type == 'expense':
            daily_spending[day_str] += transaction.amount
        elif transaction.transaction_type == 'income':
            daily_income[day_str] += transaction.amount

    # Debugging: Print populated daily_spending and daily_income
    print("Populated Daily Spending (Last 30 Days):", daily_spending)
    print("Populated Daily Income (Last 30 Days):", daily_income)

    # Calculate cumulative spending and income
    cumulative_spending = []
    cumulative_income = []
    total_spending = Decimal('0.00')
    total_income = Decimal('0.00')
    for day in labels:
        day_with_year = f"{day} {current_date.year}"  # Example: "01 May 2023"
        day_str = datetime.strptime(day_with_year, "%d %b %Y").strftime("%Y-%m-%d")
        print(f"Day: {day}, Day with Year: {day_with_year}, Day String: {day_str}")
        total_spending += daily_spending.get(day_str, Decimal('0.00'))
        total_income += daily_income.get(day_str, Decimal('0.00'))
        cumulative_spending.append(float(total_spending))  # Convert to float for Chart.js
        cumulative_income.append(float(total_income))  # Convert to float for Chart.js

    # Debugging: Print cumulative spending and income
    print("Cumulative Spending (Last 30 Days):", cumulative_spending)
    print("Cumulative Income (Last 30 Days):", cumulative_income)

    # Calculate total expenses and income for the last 30 days
    total_expenses = float(total_spending)
    total_income = float(total_income)
    net_balance = total_income - total_expenses
    # Get the current budget
    try:
        current_budget = Budget.objects.latest('created_at')
        budget_amount = current_budget.amount
    except Budget.DoesNotExist:
        budget_amount = 0

    # Calculate remaining budget (budget - expenses of last 30 days)
    remaining_budget = budget_amount - Decimal(total_expenses)


    # Fetch recent and past transactions
    recent_transactions = Transaction.objects.filter(
        user=request.user,
        date__range=[start_date, current_date]
    ).order_by("-date")

    past_transactions = Transaction.objects.filter(
        user=request.user,
        date__lt=start_date
    ).order_by("-date")

    # Debugging: Print recent and past transactions
    print("Recent Transactions:")
    for transaction in recent_transactions:
        print(f"ID: {transaction.id}, Date: {transaction.date}, Type: {transaction.transaction_type}, Amount: {transaction.amount}")

    print("Past Transactions:")
    for transaction in past_transactions:
        print(f"ID: {transaction.id}, Date: {transaction.date}, Type: {transaction.transaction_type}, Amount: {transaction.amount}")

    # Pass data to the template
    context = {
        'username': request.user.first_name if request.user.first_name else request.user.username,
        'total_expenses': total_expenses,
        'total_income': total_income,
        'net_balance': net_balance,
        'recent_transactions': recent_transactions,
        'past_transactions': past_transactions,
        'form': form,
        'daily_spending': daily_spending,  # Daily spending data
        'daily_income': daily_income,  # Daily income data
        'labels': labels,  # Days of the last 30 days
        'cumulative_spending': cumulative_spending,  # Cumulative spending data
        'cumulative_income': cumulative_income,  # Cumulative income data
    }
    return render(request, "tracker/transaction_history.html", context)


def set_budget(request):
    if request.method == 'POST':
        budget_amount = request.POST.get('budget_amount')

        print(f"Received budget amount: {budget_amount}")  # Debugging output

        if budget_amount:
            new_budget = Budget.objects.create(amount=float(budget_amount))
            print(f"New budget saved: ID={new_budget.id}, Amount={new_budget.amount}")  # Debugging output

        return redirect('transaction_history')
    return redirect('transaction_history')

@login_required
def home(request):
    # Get the current date and the first day of the current month
    today = datetime.now()
    first_day_of_month = today.replace(day=1)

    # Fetch all transactions for the logged-in user in the current month
    transactions = Transaction.objects.filter(
        user=request.user,
        date__gte=first_day_of_month,  # Transactions from the first day of the month
        date__lte=today  # Transactions up to today
    ).order_by("date")

    # Debugging: Print all transactions
    print("All Transactions (Current Month):")
    for transaction in transactions:
        print(f"ID: {transaction.id}, Date: {transaction.date}, Type: {transaction.transaction_type}, Amount: {transaction.amount}, Category: {transaction.category}")

    # Initialize data structures
    daily_spending = {}
    daily_income = {}
    cumulative_spending = []
    cumulative_income = []
    labels = []  # Days of the month

    # Initialize daily spending and income to 0 for each day of the month
    current_day = first_day_of_month
    while current_day <= today:
        day_str = current_day.strftime("%Y-%m-%d")
        daily_spending[day_str] = Decimal('0.00')
        daily_income[day_str] = Decimal('0.00')
        labels.append(current_day.strftime("%d %b"))  # Format: "01 May", "02 May", etc.
        current_day += timedelta(days=1)

    # Debugging: Print initialized daily_spending and daily_income
    print("Initialized Daily Spending (Current Month):", daily_spending)
    print("Initialized Daily Income (Current Month):", daily_income)

    # Populate daily spending and income
    for transaction in transactions:
        day_str = transaction.date.strftime("%Y-%m-%d")
        if transaction.transaction_type == 'expense':
            daily_spending[day_str] += transaction.amount
        elif transaction.transaction_type == 'income':
            daily_income[day_str] += transaction.amount

    # Debugging: Print populated daily_spending and daily_income
    print("Populated Daily Spending (Current Month):", daily_spending)
    print("Populated Daily Income (Current Month):", daily_income)

    # Calculate cumulative spending and income
    total_spending = Decimal('0.00')
    total_income = Decimal('0.00')
    for day in labels:
        day_with_year = f"{day} {today.year}"  # Example: "01 May 2023"
        day_str = datetime.strptime(day_with_year, "%d %b %Y").strftime("%Y-%m-%d")
        print(f"Day: {day}, Day with Year: {day_with_year}, Day String: {day_str}")
        total_spending += daily_spending.get(day_str, Decimal('0.00'))
        total_income += daily_income.get(day_str, Decimal('0.00'))
        cumulative_spending.append(float(total_spending))  # Convert to float for Chart.js
        cumulative_income.append(float(total_income))  # Convert to float for Chart.js

    # Debugging: Print cumulative spending and income
    print("Cumulative Spending (Current Month):", cumulative_spending)
    print("Cumulative Income (Current Month):", cumulative_income)

    # Calculate spending by category for the pie chart
    spending_by_category = Transaction.objects.filter(
        user=request.user,
        transaction_type='expense',
        date__gte=first_day_of_month,
        date__lte=today
    ).values('category').annotate(total=Sum('amount')).order_by('-total')

    pie_labels = [item['category'] for item in spending_by_category]
    pie_data = [float(item['total']) for item in spending_by_category]

    # Debugging: Print pie chart data
    print("Pie Labels (Categories):", pie_labels)
    print("Pie Data (Spending by Category):", pie_data)

    # Pass data to the template
    context = {
        'username': request.user.first_name if request.user.first_name else request.user.username,
        'total_spending': total_spending,
        'total_earnings': total_income,
        'budget_left': total_income - total_spending,
        'months': labels,  # Days of the month (e.g., "01 May", "02 May")
        'expense_data': cumulative_spending,  # Cumulative spending data
        'income_data': cumulative_income,  # Cumulative income data
        'pie_labels': pie_labels,  # Categories for the pie chart
        'pie_data': pie_data,  # Spending amounts for the pie chart
    }
    return render(request, 'tracker/home.html', context)

def handle_chat_text(chat_text):
    # Your function to handle the chat text
    print(f"Chat text received: {chat_text}")


from .financialai import generate_transaction_data, ai_reply
from .models import Debt

from .financialai import generate_transaction_data, ai_reply
from .models import Transaction
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Sum

@login_required
def advisor(request):

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
    if request.method == 'GET':
        chat_text = request.GET.get('chat_text')
        print(1)
        if chat_text:
            print(2)
            # Fetch all transactions for the logged-in user and generate the AI response
            transaction_text = generate_transaction_data(request.user)
            ai_response = ai_reply(transaction_text, chat_text)
            print(ai_response)
            # Return the AI response
            context = {
                'transactions': transactions,
                'total_spending': total_spending,
                'total_earnings': total_earnings,
                'budget_left': budget_left,
                'response': ai_response,
                'question': chat_text,
            }
            return render(request, "tracker/advisor.html", context)

    # Fetch all transactions for the logged-in user

    return render(request, "tracker/advisor.html", context)


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


@csrf_exempt
def analyze_text(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            result = aitransaction(text)
            return JsonResponse(result)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def debt_history(request):
    # Fetch all debts related to the logged-in user
    debts = Debt.objects.filter(user=request.user)

    if request.method == "POST":
        form = DebtForm(request.POST)
        if form.is_valid():
            debt = form.save(commit=False)
            debt.user = request.user
            debt.save()
            return redirect("debt_history")
    else:
        form = DebtForm()

    context = {
        'debts': debts,
        'form': form,
    }
    return render(request, "tracker/debt_history.html", context)

def delete_debt(request, debt_id):
    debt = get_object_or_404(Debt, id=debt_id)
    debt.delete()
    return redirect('debt_history')
def delete_transaction(request, transaction_id):
    if request.method == 'POST':
        transaction = get_object_or_404(Transaction, id=transaction_id)
        transaction.delete()
        return redirect('transaction_history')

