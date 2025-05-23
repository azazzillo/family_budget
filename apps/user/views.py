# Django
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.shortcuts import render
from django.conf import settings
# Rest
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
# Local
from .serializers import(
    CustomUserSerializer, LoginSerializer, InventationSerializer,
    RegisterByInviteSerializer
)
from .models import CustomUser, Inventation
# Python
import datetime


class RegisterView(APIView):
    permission_classes = [AllowAny,]

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = authenticate(
            request=request,
            username=email,
            password=password
        )

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'detail':'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        

class InviteView(APIView):
    permission_classes = [IsAuthenticated,]

    def post(self, request):
        serializer = InventationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        
        invite = Inventation.objects.create(
            invented_by = request.user,
            email = email
        )

        host = request.get_host()
        invite_link = f"http://{host}/api/register/?token={invite.token}"

        send_mail(
            'ВАС ПРИГЛАСИЛИ В СЕМЬЮ',
            f'Пройдите по ссылке, чтобы зарегаться: {invite_link}',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False
        )

        return Response(
            {'detail': 'Invite sent'},
            status=status.HTTP_200_OK
        )


class RegisterByInviteView(APIView):
    def post(self, request):
        serializer = RegisterByInviteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data['token']
        password = serializer.validated_data['password']

        try:
            invite = Inventation.objects.get(token=token, is_used = False)
        except Inventation.DoesNotExist:
            return Response(
                {'detail': 'Invalid or user invite token!!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = CustomUser.objects.create(
            email = invite.email
        )
        user.set_password(password)
        user.save()

        invite.is_used = True
        invite.save()

        return Response(
            {'detail': 'User registraed successfully'},
            status=status.HTTP_201_CREATED
        )

