from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings

from .models import Account
from .serializers import AccountSerializer


@api_view(['POST', ])
@permission_classes([AllowAny, ])
def register_view(request):
    serializer = AccountSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', ])
def detail_view(request):
    try:
        account = request.user
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = AccountSerializer(account)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT', ])
def update_view(request):
    try:
        account = request.user
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    print("hello user:")
    print(request.user)
    serializer = AccountSerializer(account, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE', ])
def delete_view(request):
    try:
        account = request.user
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    account.is_active = False
    serializer = AccountSerializer(account, request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)
    
        
#{"email": "test@gmail.com", "password": "123"}

@api_view(['POST', ])
@permission_classes([AllowAny, ])
def login_view(request):
    import ast
    def get_tokens_for_user(user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    
    
    """ =email = request.POST['email']
    password = request.POST['password']
"""    
    # print("print body")
    
    # print("print post")
    # print(request.POST)

    dict = ast.literal_eval(request.body.decode("UTF-8"))
    email = dict['email']
    password = dict['password']

    print(email)
    print(password)
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

@api_view(['GET', ])
@permission_classes([AllowAny, ])
def verify_view(request):
    # This is possible because JWT authentication backend check whether user's token is valid or not
    # possible return codes
    # 200, 401, 404
    if request.method == 'GET':
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_404_NOT_FOUND)
