# Django
from rest_framework import serializers
# Local
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Transaction
        fields = [
            'id', 
            'user',
            'amount',
            'type',
            'category',
            'comment',
            'datetime_created'
        ]
        read_only_fields = [
            'id',
            'datetime_created'
        ]
        extra_kwargs = {
            'comment': {
                'required': False, 
                'allow_blank': True,
                'allow_null': True
            }
        }
