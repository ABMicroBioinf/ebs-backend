from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from account.models import Account

from .serializers import AccountSerializer


@api_view(['POST', ])
def register_view(request):
    if request.method == 'POST':
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', ])
def detail_view(request, email):
    try:
        account = Account.objects.get(email=email)
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializers = AccountSerializer(account)
        return Response(serializers.data)


@api_view(['PUT', ])
def update_view(request, email):
    try:
        account = Account.objects.get(email=email)
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializers = AccountSerializer(account, data=request.data)
        data = {}
        if serializers.is_valid():
            serializers.save()
            data["response"] = "update successful"
            return Response(data=data)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE', ])
def delete_view(request, email):
    try:
        account = Account.objects.get(email=email)
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
def login_view(request):
    pass


@api_view(['GET', ])
def logout_view(request):
    pass
