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
def login_view(request):
    pass


@api_view(['GET', ])
def logout_view(request):
    pass
