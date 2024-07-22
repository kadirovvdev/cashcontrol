from django.db import models
from users.models import CustomUser


class AccountBalance(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def update_balance(self):
        income_total = Income.total_income(self.user)
        expenses_total = Expense.total_expenses(self.user)
        self.balance = income_total - expenses_total
        self.save()

class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('Cafe', 'Cafe'),
        ('Groceries', 'Groceries'),
        ('Transport', 'Transport'),
        ('Entertainment', 'Entertainment'),
        ('Utilities', 'Utilities'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)

    @classmethod
    def total_expenses(cls, user):
        return cls.objects.filter(user=user).aggregate(total=models.Sum('amount'))['total'] or 0

    def __str__(self):
        return f'{self.category} - {self.amount} on {self.date}'


class Income(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)

    @classmethod
    def total_income(cls, user):
        return cls.objects.filter(user=user).aggregate(total=models.Sum('amount'))['total'] or 0
