# ExpenseWise - Expense Tracker

## Overview
This project is an expense tracker application built using Django. It allows users to track their income and expenses, view transaction history, manage budgets, and get financial advice through an AI-powered advisor.

## Features
- **User Authentication**: Secure login and registration.
- **Transaction Management**: Add, view, and delete income and expense transactions.
- **Budget Management**: Set and view budgets.
- **Financial Analysis**: View daily, monthly, and cumulative spending and income.
- **AI Advisor**: Get financial advice based on transaction history.
- **Debt Management**: Track and manage debts.

## Technologies Used
- **Backend**: Django, Python
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite (default for Django)
- **AI Integration**: Custom AI models for financial advice

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/LimJames180/expense-tracker.git
    cd expense-tracker
    ```

2. **Create a virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Apply migrations**:
    ```bash
    python manage.py migrate
    ```

5. **Create a superuser**:
    ```bash
    python manage.py createsuperuser
    ```

6. **Run the development server**:
    ```bash
    python manage.py runserver
    ```

7. **Access the application**:
    Open your web browser and go to `http://127.0.0.1:8000`.

## Usage

### Home Page
- View cumulative spending and income for the current month.
- View spending by category in a pie chart.

### Transaction History
- Add new transactions (income or expense).
- View recent transactions and past transactions.
- Delete transactions.

### Budget Management
- Set a new budget.
- View remaining budget based on current spending.

### AI Advisor
- Get financial advice by interacting with the AI advisor.
- View chat history and AI responses.

### Debt Management
- Add and view debts.
- Delete debts.

## Contributing
1. **Fork the repository**.
2. **Create a new branch**:
    ```bash
    git checkout -b feature-branch
    ```
3. **Make your changes**.
4. **Commit your changes**:
    ```bash
    git commit -m "Description of changes"
    ```
5. **Push to the branch**:
    ```bash
    git push origin feature-branch
    ```
6. **Create a pull request**.

## License
This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Contact
For any inquiries or issues, please contact LimJames180 on GitHub.
