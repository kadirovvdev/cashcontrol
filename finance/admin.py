from django.contrib import admin
from .models import Expense, AccountBalance, Income
admin.site.register(Expense)
admin.site.register(AccountBalance)
admin.site.register(Income)


