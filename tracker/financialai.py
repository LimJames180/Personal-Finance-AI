# ! pip install -U cohere
import os

import cohere
from pycparser.ply.yacc import LRGeneratedTable

from tracker.models import Transaction, Debt  # Use absolute import
api_key = os.getenv('COHERE_API_KEY')
co = cohere.ClientV2(
    api_key
)  # Get your free API key here: https://dashboard.cohere.com/api-keys


def ai_reply(context, debts, message):

    documents = [
        {
            "data": {
                "title": "Transaction History",
                "text": context
            }
        },

    ]

    # Add the user message
    messages = [{"role": "user", "content": "act as a financial advisor do not say you are an AI/LLM \n these are my financial data \n" + context + "\n here are my debt data" + debts + "\n" + message}]

    response = co.chat(
        model="4b8a19b2-55f1-444a-93d5-79ff8925d77f-ft",
        messages=messages,
    )

    return response.message.content[0].text



from tracker.models import Transaction

def generate_transaction_data(user):
    # Fetch all transactions for the given user
    transactions = Transaction.objects.filter(user=user).order_by("-date")

    # Format the transaction data into a text string
    transaction_texts = []
    for transaction in transactions:
        date_str = transaction.date.strftime("%Y-%m-%d")
        amount_str = f"{transaction.amount:.2f}"
        transaction_text = f"Date: {date_str}, Amount: {amount_str}, Type: {transaction.transaction_type}, Category: {transaction.category}"
        transaction_texts.append(transaction_text)

    # Join all transaction texts into a single string
    formatted_text = "\n".join(transaction_texts)
    return formatted_text

def generate_debt_data(user):
    debts = Debt.objects.filter(user=user).order_by("-status")
    debt_texts = []
    for debt in debts:
        debt_text = (
            f"Debt Name: {debt.debt_name}, "
            f"Creditor: {debt.creditor}, "
            f"Total Amount Owed: {debt.total_amount_owed:.2f}, "
            f"Minimum Monthly Payment: {debt.minimum_monthly_payment:.2f}, "
            f"Interest Rate: {debt.interest_rate:.2f}, "
            f"Due Date: {debt.due_date.strftime('%Y-%m-%d')}, "
            f"Monthly Due Day: {debt.monthly_due_day.strftime('%Y-%m-%d')}, "
            f"Status: {'Active' if debt.status else 'Paid off'}, "
            f"Notes: {debt.notes}"
        )
        debt_texts.append(debt_text)

    # Join all debt texts into a single string
    formatted_text = "\n".join(debt_texts)
    return formatted_text
