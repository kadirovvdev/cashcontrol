from django.db import models


class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('Cafe', 'Cafe'),
        ('Groceries', 'Groceries'),
        ('Transport', 'Transport'),
        ('Entertainment', 'Entertainment'),
        ('Utilities', 'Utilities'),
    ]

    date = models.DateField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)

    @classmethod
    def total_expenses(cls):
        return cls.objects.aggregate(total=models.Sum('amount'))['total'] or 0

    def __str__(self):
        return f'{self.category} - {self.amount} on {self.date}'
