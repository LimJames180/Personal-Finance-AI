from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["amount", "category", "date", "description", "transaction_type"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "transaction_type": forms.RadioSelect(choices=[("expense", "Expense"), ("income", "Income")]),
        }
