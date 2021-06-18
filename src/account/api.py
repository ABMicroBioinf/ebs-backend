from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings

from .models import Account

from .serializers import AccountSerializer


@api_view(['POST', ])
@permission_classes([AllowAny, ])
def register_view(request):
    if request.method == 'POST':
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid(): 
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', ])
def detail_view(request, slug):
    try:
        account = Account.objects.get(username=slug)
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AccountSerializer(account)
        return Response(serializer.data)


@api_view(['PUT', ])
def update_view(request, slug):
    try:
        account = Account.objects.get(username=slug)
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = AccountSerializer(account, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_204_NO_CONTENT)


@api_view(['DELETE', ])
def delete_view(request, slug):
    try:
        account = Account.objects.get(username=slug)
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        operation = account.delete()
        data = {}
        if operation:
            data["response"] = "delete successful"
        else:
            data["response"] = "delete failed"
        return Response(data=data)


@api_view(['POST', ])
@permission_classes([AllowAny, ])
def login_view(request):

    def get_tokens_for_user(user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        print(user)
        if user:
            data = get_tokens_for_user(user)
            res = Response(data, status=status.HTTP_200_OK)
            res.set_cookie(
                value=data['access'],
                key=settings.SIMPLE_JWT['AUTH_COOKIE'],
                expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
            )
            return res
        return Response(status=status.HTTP_404_NOT_FOUND)


""" @api_view(['GET', ])
def logout_view(request):
    print('hi')
    pass """