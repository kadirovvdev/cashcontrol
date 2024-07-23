from datetime import timedelta, date
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.views import View
from django.views.generic import ListView
from .models import Expense, Income, AccountBalance
from .forms import ExpenseForm, IncomeForm

class ExpenseListView(ListView):
    model = Expense
    template_name = 'dashboard.html'
    context_object_name = 'expenses'
    ordering = ['-date']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_expenses = Expense.objects.filter(user=self.request.user).order_by('-date')

        today = now().date()
        start_of_week = today - timedelta(days=today.weekday())
        start_of_month = today.replace(day=1)
        start_of_year = today.replace(month=1, day=1)

        context['daily_expenses'] = user_expenses.filter(date=today)
        context['weekly_expenses'] = user_expenses.filter(date__gte=start_of_week)
        context['monthly_expenses'] = user_expenses.filter(date__gte=start_of_month)
        context['yearly_expenses'] = user_expenses.filter(date__gte=start_of_year)

        context['total_daily'] = context['daily_expenses'].aggregate(total=Sum('amount'))['total'] or 0
        context['total_weekly'] = context['weekly_expenses'].aggregate(total=Sum('amount'))['total'] or 0
        context['total_monthly'] = context['monthly_expenses'].aggregate(total=Sum('amount'))['total'] or 0
        context['total_yearly'] = context['yearly_expenses'].aggregate(total=Sum('amount'))['total'] or 0

        # For calendar search
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        if date_from and date_to:
            context['filtered_expenses'] = user_expenses.filter(date__range=[date_from, date_to])

        return context


class IncomeListView(ListView):
    model = Income
    template_name = 'income_list.html'
    context_object_name = 'incomes'
    ordering = ['-date']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_incomes = Income.objects.filter(user=self.request.user).order_by('-date')

        context['incomes'] = user_incomes
        context['total_income'] = user_incomes.aggregate(total=Sum('amount'))['total'] or 0

        return context

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
