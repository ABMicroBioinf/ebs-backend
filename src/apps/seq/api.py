from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
)
from rest_framework.viewsets import GenericViewSet

from apps.seq.models import MetadataFile, SeqFile, Study, Run
from .serializers import StudySerializer, RunSerializer, SeqFileSerializer, MetadataFileSerializer


class StudyViewSet(GenericViewSet,  # generic view functionality
                     CreateModelMixin,  # handles POSTs
                     RetrieveModelMixin,  # handles GETs for 1 Company
                     UpdateModelMixin,  # handles PUTs and PATCHes
                     ListModelMixin,  # handles GETs for many Companies
                     DestroyModelMixin,): #handle delete
 
      serializer_class = StudySerializer
      queryset = Study.objects.all()

      # This method should be overriden
      # if we dont want to modify query set based on current instance attributes
      def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

      def perform_create(self, serializer):
            serializer.save(owner=self.request.user)

class RunViewSet(GenericViewSet,  # generic view functionality
                     CreateModelMixin,  # handles POSTs
                     RetrieveModelMixin,  # handles GETs for 1 Company
                     UpdateModelMixin,  # handles PUTs and PATCHes
                     ListModelMixin,  # handles GETs for many Companies
                     DestroyModelMixin,): #handle delete

      serializer_class = RunSerializer
      queryset = Run.objects.all()
      
      # This method should be overriden
      # if we dont want to modify query set based on current instance attributes
      def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

      def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SeqFileViewSet(GenericViewSet,  # generic view functionality
                     CreateModelMixin,  # handles POSTs
                     RetrieveModelMixin,  # handles GETs for 1 Company
                     UpdateModelMixin,  # handles PUTs and PATCHes
                     ListModelMixin,  # handles GETs for many Companies
                     DestroyModelMixin,): #handle delete
      serializer_class = SeqFileSerializer
      queryset = SeqFile.objects.all()

class MetadataFileViewSet(GenericViewSet,  # generic view functionality
                     CreateModelMixin,  # handles POSTs
                     RetrieveModelMixin,  # handles GETs for 1 Company
                     UpdateModelMixin,  # handles PUTs and PATCHes
                     ListModelMixin,  # handles GETs for many Companies
                     DestroyModelMixin,): #handle delete

      serializer_class = MetadataFileSerializer
      queryset = MetadataFile.objects.all()


from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from .serializers import MyFileSerializer


class MyFileUploadViewSet(viewsets.ViewSet):

    def create(self, request):
        serializer_class = MyFileSerializer(data=request.data)
        if 'file' not in request.FILES or not serializer_class.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            #Single File
            #handle_uploaded_file(request.FILES['file'])

            #Multiple Files
            files = request.FILES.getlist('file')
            for f in files:
                handle_uploaded_file(f)

            return Response(status=status.HTTP_201_CREATED)

def handle_uploaded_file(f):
    with open(f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)