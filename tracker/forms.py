from django import forms
from .models import Transaction,Debt

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["amount", "category", "date", "description", "transaction_type"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "transaction_type": forms.RadioSelect(choices=[("expense", "Expense"), ("income", "Income")]),
        }

class DebtForm(forms.ModelForm):
    class Meta:
        model = Debt
        fields = ['debt_name', 'creditor', 'total_amount_owed', 'minimum_monthly_payment', 'interest_rate', 'due_date', 'monthly_due_day', 'status', 'notes']