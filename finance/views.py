from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView

from .models import Expense
from .forms import ExpenseForm

# def dashboard(request):
#     expenses = Expense.objects.all()
#     total_amount = sum(expense.amount for expense in expenses)
#     context = {
#         'expenses': expenses,
#         'total_amount': total_amount
#     }
#     return render(request, 'dashboard.html', context)
class ExpenseListView(ListView):
    model = Expense
    template_name = 'dashboard.html'
    context_object_name = 'expenses'
    ordering = ['-date']

# def add_expense(request):
#     if request.method == 'POST':
#         form = ExpenseForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('dashboard')
#     else:
#         form = ExpenseForm()
#     return render(request, 'add_expense.html', {'form': form})

# views.py

# from django.shortcuts import render, redirect
# from .forms import ExpenseForm
# from .models import Expense


def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ExpenseForm()

    total_expenses = Expense.total_expenses()
    return render(request, 'add_expense.html', {'form': form, 'total_expenses': total_expenses})


def dashboard(request):
    total_balance = 90800  # Example static balance
    total_income = 1200000  # Example static income
    total_expenses = Expense.total_expenses()

    expenses = Expense.objects.all()

    context = {
        'total_balance': total_balance,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'expenses': expenses,
    }

    return render(request, 'dashboard.html', context)
