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
