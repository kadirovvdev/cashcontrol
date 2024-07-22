from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard/', ExpenseListView.as_view(), name='dashboard'),
    path('add_expense/', add_expense, name='add_expense'),
]
