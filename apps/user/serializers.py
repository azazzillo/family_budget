# Django
from rest_framework import serializers
# Local
from .models import CustomUser, Inventation


class CustomUserSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = CustomUser
        fields = [
            'id',
            'name',
            'email',
            'password',
            'position',
            'age',
            'is_owner'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
            instance.save()
            return instance


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class InventationSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Inventation
        fields = [
            'id',
            'invented_by',
            'email',
            'token',
            'is_used',
            'datetime_created'
        ]
        read_only_fields = [
            'id',
            'invented_by',
            'token',
            'is_used',
            'datetime_created'
        ]
    
    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("User already have family :(")
        return value
    

class RegisterByInviteSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField(write_only=True)
