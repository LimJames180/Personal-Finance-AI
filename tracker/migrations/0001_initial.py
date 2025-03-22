# Generated by Django 5.1.1 on 2025-03-22 14:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Transaction",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "category",
                    models.CharField(
                        choices=[
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
                        ],
                        max_length=20,
                    ),
                ),
                ("date", models.DateField()),
                ("description", models.CharField(max_length=255)),
                (
                    "transaction_type",
                    models.CharField(
                        choices=[("expense", "Expense"), ("income", "Income")],
                        max_length=10,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
