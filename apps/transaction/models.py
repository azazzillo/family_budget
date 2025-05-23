# Django
from django.db import models
from django.utils import timezone
# Local
from user.models import CustomUser, FamilyUser, Family


class Category(models.Model):

    name = models.CharField(
        verbose_name='название категории',
        max_length=120,
        null=False,
        unique=True
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
    
    def __str__(self) -> str:
        return f'{self.name}'


class Transaction(models.Model):

    class Type(models.TextChoices):
        EXPENSES = 'EXPENSES', 'Expenses'
        INCOME = 'INCOME', 'Income'

    user = models.ForeignKey(
        to=CustomUser,
        verbose_name="пользователь",
        related_name="пользователь_транзакции",
        on_delete=models.CASCADE
    )
    amount = models.DecimalField(
        verbose_name="сумма",
        max_digits=11,
        decimal_places=2
    )
    type = models.CharField(
        verbose_name="тип",
        max_length=20,
        choices=Type.choices,
        default=Type.EXPENSES
    )
    category = models.ForeignKey(
        to=Category,
        verbose_name="категория",
        related_name="категория_транзакции",
        on_delete=models.CASCADE
    )
    comment = models.CharField(
        verbose_name="комментарий",
        max_length=250,
        null=True
    )
    datetime_created = models.DateField(
        verbose_name="дата",
        default=timezone.now
    )

    class Meta:
        verbose_name = "транзакция"
        verbose_name_plural = "транзакции"

    def __str__(self):
        return f"{self.amount} ({self.type}) category: {self.category}| {self.user} | {self.datetime_created} "



