# Django
from django.shortcuts import render
from django.db.models import Sum
# Rest
from rest_framework.permissions import IsAuthenticated
from rest_framework.validators import ValidationError
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
# Local
from .permissions import IsFamilyMember
from .serializers import TransactionSerializer
from .models import Transaction
from .models import FamilyUser


class TransactionViewSet(ModelViewSet):
    queryset=Transaction.objects.all()
    serializer_class=TransactionSerializer
    permission_classe=[IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        family_which = FamilyUser.objects.filter(member=user)

        if not family_which.exists():
            return Transaction.objects.none()
        
        family = family_which.first().family
        all_family_members = FamilyUser.objects.filter(family=family).values_list('member_id', flat=True)

        return Transaction.objects.filter(user__id__in=all_family_members)

    def perform_create(self, serializer):
        transaction = serializer.save(user = self.request.user)

        family_user = FamilyUser.objects.filter(member=self.request.user).first()
        family = family_user.family

        if transaction.type == 'INCOME':
            if transaction.amount > family.wallet_amount:
                raise ValidationError("Недостаточно средств в общем кошельке семьи")
            family.wallet_amount += transaction.amount
        elif transaction.type == 'EXPENSES':
            family.wallet_amount -= transaction.amount

        family.save()

        return super().perform_create(serializer)

    @action(
        detail=False, methods=['get'], url_path='summary',
        permission_classes=[IsAuthenticated, IsFamilyMember])
    def summary(self, request):
        user = request.user

        family_user = FamilyUser.objects.filter(member=user).first()
        if not family_user:
            return Response({'detail': 'У вас нет семьи'}, status=403)

        family = family_user.family
        all_family_members = FamilyUser.objects.filter(family=family).values_list('member_id', flat=True)

        transactions = Transaction.objects.filter(user__id__in=all_family_members)

        income = transactions.filter(type='INCOME').aggregate(total=Sum('amount'))['total'] or 0
        expenses = transactions.filter(type='EXPENSES').aggregate(total=Sum('amount'))['total'] or 0

        return Response({
            "income": income,
            "expenses": expenses,
            "balance": family.wallet_amount
        })

