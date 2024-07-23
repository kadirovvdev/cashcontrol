from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from users.models import CustomUser
from finance.models import *


@login_required(login_url="users/login/")
def landing_page(request):
    user = request.user

    try:
        account_balance = AccountBalance.objects.get(user=user)
        total_balance = account_balance.balance
    except AccountBalance.DoesNotExist:
        total_balance = 0

    total_income = Income.total_income(user)
    total_expenses = Expense.total_expenses(user)
    expenses = Expense.objects.filter(user=user)

    context = {
        'total_balance': total_balance,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'expenses': expenses,
    }

    return render(request, 'landing_page.html', context)
