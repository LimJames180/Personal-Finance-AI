from django.db import models
from django.contrib.auth.models import User

CATEGORY_CHOICES = [
    ("Food", "Food"),
    ("Housing", "Housing"),
    ("Transportation", "Transportation"),
    ("Health", "Health"),
    ("Entertainment", "Entertainment"),
    ("Shopping", "Shopping"),
    ("Bills", "Bills"),
    ("Travel", "Travel"),
    ("Education", "Education"),
    ("Finance", "Finance"),
    ("Donations", "Donations"),
    ("Miscellaneous", "Miscellaneous"),
    ("Income", "Income"),
]

TRANSACTION_TYPE_CHOICES = [
    ("expense", "Expense"),
    ("income", "Income"),
]

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    date = models.DateField()
    description = models.CharField(max_length=255)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.transaction_type} - {self.amount}"


class Debt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    debt_name = models.CharField(max_length=255)  # Name of the debt
    creditor = models.CharField(max_length=255, blank=True, null=True)  # Optional creditor name
    total_amount_owed = models.FloatField()  # Total amount owed
    minimum_monthly_payment = models.FloatField()  # Minimum monthly payment
    interest_rate = models.FloatField()  # Interest rate
    due_date = models.DateTimeField()  # Due date for the debt
    monthly_due_day = models.DateTimeField()  # Specific monthly due day
    status = models.BooleanField(default=True)  # Active (True) or Paid off (False)
    notes = models.TextField(blank=True, null=True)  # Optional notes

    def __str__(self):
        return self.name
