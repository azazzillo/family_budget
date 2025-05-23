# Django
from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone
from django.db import models
# Python
import datetime
import uuid


class CustomUserManager(BaseUserManager):
    def get_by_natural_key(self, email):
        return self.get(email=email)


class CustomUser(AbstractBaseUser):

    class Position(models.TextChoices):
        PARENT = "PARENT", "Parent"
        CHILD = "CHILD", "Child"
        GRANDPARENT = "GRANDPARENT", "Grandparent"
        PET = "PET", "Pet"

    name = models.CharField(
        verbose_name="имя",
        max_length=50,
        null=False
    )
    email = models.EmailField(
        verbose_name="почта",
        null=False,
        unique=True
    )
    position = models.CharField(
        verbose_name="позиция",
        max_length=100,
        choices=Position.choices,
        default=Position.PARENT
    )
    age = models.IntegerField(
        verbose_name="возраст",
        default=25
    )
    is_owner = models.BooleanField(
        verbose_name="является ли владельцем",
        default=False
    )

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return f"{self.name} ({self.position})"
    

class Family(models.Model):

    name = models.CharField(
        verbose_name="название",
        max_length=200,
        null=False,
        default="Family"
    )
    owner = models.ForeignKey(
        to=CustomUser,
        verbose_name="владелец",
        related_name="владелец_семьи",
        on_delete=models.CASCADE
    )
    datetime_created = models.DateTimeField(
        verbose_name="дата создания",
        default=timezone.now,
    )
    wallet_amount = models.DecimalField(
        verbose_name="сумма общего кошелька",
        max_digits=11,
        decimal_places=2,
        default=0.00
    )

    class Meta:
        verbose_name = 'семья'
        verbose_name_plural = 'семьи'
    
    def __str__(self):
        return f"{self.name} владелец: {self.owner} | {self.wallet_amount}"


class FamilyUser(models.Model):

    family = models.ForeignKey(
        to=Family,
        verbose_name="семья",
        related_name="семья_связь",
        on_delete=models.CASCADE
    )
    member = models.ForeignKey(
        to=CustomUser,
        verbose_name="член семьи",
        related_name="член_семьи_связь",
        on_delete=models.CASCADE
    )

    class Meta: 
        verbose_name = 'член семьи'
        verbose_name_plural = 'члены семьи'


class Inventation(models.Model):
    invented_by = models.ForeignKey(
        to=CustomUser,
        verbose_name='приглашающий',
        related_name='приглашающий_кто',
        on_delete=models.CASCADE
    )
    email = models.EmailField(
        verbose_name='почта'
    )
    token = models.UUIDField(
        default=uuid.uuid4,
        unique=True
    )
    is_used = models.BooleanField(
        verbose_name='статус',
        default=False
    )
    datetime_created = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'приглашение'
        verbose_name_plural = 'приглашения'
