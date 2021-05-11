from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import CreateStudySerializer, DetailStudySerializer, EditStudySerializer


@api_view(['POST',])
def create_study_view(request):
    if request.method == 'POST':
        serializer = CreateStudySerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            # study = serializer.save()
            data['response'] = "Successfully created a new study."
            # data['email'] = account.email
            # data['username'] = account.username
        else:
            data = serializer.errors
        return Response(data)