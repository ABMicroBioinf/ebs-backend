from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import LoginSerializer, RegistrationSerializer


@api_view(['GET', 'POST'])
def login_view(request):
    # GET Mapping; It will be removed
    if request.method == 'GET':
        return Response("login view")
    # POST Mapping
    elif request.method == 'POST':
        serializer = LoginSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
        else:
            data = serializer.errors
        return Response(data)

@api_view(['GET',])
def logout_view(request):
    if request.method == 'GET':
        return Response("You will be redirected to main page")

@api_view(['GET', 'POST',])
def registration_view(request):
    # GET Mapping; It will be removed
    if request.method == 'GET':
        return Response("Display registration form here")
    # POST Mapping
    elif request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = "Successfully registered a new user."
            data['email'] = account.email
            data['username'] = account.username
        else:
            data = serializer.errors
        return Response(data)

@api_view(['GET',])
def overview_view(request):
    if request.method == 'GET':
        return Response("An account information will be returned")
