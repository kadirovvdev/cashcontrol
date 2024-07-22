from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView

from .models import Expense, Income, AccountBalance
from .forms import ExpenseForm, IncomeForm

class ExpenseListView(ListView):
    model = Expense
    template_name = 'dashboard.html'
    context_object_name = 'expenses'
    ordering = ['-date']

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user).order_by('-date')


class IncomeListView(ListView):
    model = Income
    template_name = 'income_list.html'
    context_object_name = 'incomes'
    ordering = ['-date']

    def get_queryset(self):
        return Income.objects.filter(user=self.request.user).order_by('-date')


def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()

            account_balance, created = AccountBalance.objects.get_or_create(user=request.user)
            account_balance.update_balance()

            return redirect('income_list')
    else:
        form = IncomeForm()

    total_income = Income.total_income(request.user)
    return render(request, 'add_income.html', {'form': form, 'total_income': total_income})
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()

            account_balance, created = AccountBalance.objects.get_or_create(user=request.user)
            account_balance.update_balance()

            return redirect('dashboard')
    else:
        form = ExpenseForm()

    total_expenses = Expense.total_expenses(request.user)
    return render(request, 'add_expense.html', {'form': form, 'total_expenses': total_expenses})

def dashboard(request):
    total_balance = AccountBalance.objects.get(user=request.user).balance
    total_income = Income.total_income(request.user)
    total_expenses = Expense.total_expenses(request.user)

    expenses = Expense.objects.filter(user=request.user)

    context = {
        'total_balance': total_balance,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'expenses': expenses,
    }

    return render(request, 'dashboard.html', context)
