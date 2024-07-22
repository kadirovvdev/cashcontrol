from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard/', ExpenseListView.as_view(), name='dashboard'),
    path('add_expense/', add_expense, name='add_expense'),
    path('add_income/', add_income, name='add_income'),
    path('incomes/', IncomeListView.as_view(), name='income_list'),
]
