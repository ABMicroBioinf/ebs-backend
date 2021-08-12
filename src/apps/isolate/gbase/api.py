from rest_framework.mixins import (
    CreateModelMixin, 
    ListModelMixin, 
    RetrieveModelMixin, 
    UpdateModelMixin, 
    DestroyModelMixin
)
from rest_framework.viewsets import GenericViewSet
from rest_framework.filters import OrderingFilter, SearchFilter
from gizmos.pagination import CustomPagination
from .models import Genome, Annotation, Virulome, Mlst, Resistome
from .serializers import (
  GenomeSerializer, 
  AnnotationSerializer, 
  VirulomeSerializer, 
  MlstSerializer, 
  ResistomeSerializer
)


class GenomeViewSet(GenericViewSet,  # generic view functionality
                     CreateModelMixin,  # handles POSTs
                     RetrieveModelMixin,  # handles GETs for 1 Company
                     UpdateModelMixin,  # handles PUTs and PATCHes
                     ListModelMixin,  # handles GETs for many Companies
                     DestroyModelMixin,): #handle delete

      serializer_class = GenomeSerializer
      queryset = Genome.objects.all()
      pagination_class = CustomPagination
      filter_backends = (SearchFilter, OrderingFilter)
      search_fields = "__all__"
      ordering_fields = "__all__"
      
      # This method should be overriden
      # if we dont want to modify query set based on current instance attributes
      def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

      def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class VirulomeViewSet(GenericViewSet,  # generic view functionality
                     CreateModelMixin,  # handles POSTs
                     RetrieveModelMixin,  # handles GETs for 1 Company
                     UpdateModelMixin,  # handles PUTs and PATCHes
                     ListModelMixin,  # handles GETs for many Companies
                     DestroyModelMixin,): #handle delete

      serializer_class = VirulomeSerializer
      queryset = Virulome.objects.all()
      pagination_class = CustomPagination
      filter_backends = (SearchFilter, OrderingFilter)
      search_fields = "__all__"
      ordering_fields = "__all__"
      
      
      # This method should be overriden
      # if we dont want to modify query set based on current instance attributes
      def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

      def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ResistomeViewSet(GenericViewSet,  # generic view functionality
                     CreateModelMixin,  # handles POSTs
                     RetrieveModelMixin,  # handles GETs for 1 Company
                     UpdateModelMixin,  # handles PUTs and PATCHes
                     ListModelMixin,  # handles GETs for many Companies
                     DestroyModelMixin,): #handle delete

      serializer_class = ResistomeSerializer
      queryset = Resistome.objects.all()
      pagination_class = CustomPagination
      filter_backends = (SearchFilter, OrderingFilter)
      search_fields = "__all__"
      ordering_fields = "__all__"
      
      
      # This method should be overriden
      # if we dont want to modify query set based on current instance attributes
      def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

      def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class MlstViewSet(GenericViewSet,  # generic view functionality
                     CreateModelMixin,  # handles POSTs
                     RetrieveModelMixin,  # handles GETs for 1 Company
                     UpdateModelMixin,  # handles PUTs and PATCHes
                     ListModelMixin,  # handles GETs for many Companies
                     DestroyModelMixin,): #handle delete

      serializer_class = MlstSerializer
      queryset = Mlst.objects.all()
      pagination_class = CustomPagination
      filter_backends = (SearchFilter, OrderingFilter)
      search_fields = "__all__"
      ordering_fields = "__all__"
      
      # This method should be overriden
      # if we dont want to modify query set based on current instance attributes
      def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

      def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class AnnotationViewSet(GenericViewSet,  # generic view functionality
                     CreateModelMixin,  # handles POSTs
                     RetrieveModelMixin,  # handles GETs for 1 Company
                     UpdateModelMixin,  # handles PUTs and PATCHes
                     ListModelMixin,  # handles GETs for many Companies
                     DestroyModelMixin,): #handle delete

      serializer_class = AnnotationSerializer
      queryset = Annotation.objects.all()
      
      pagination_class = CustomPagination
      pagination_class.page_size = 1
      filter_backends = (SearchFilter, OrderingFilter)
      search_fields = "__all__"
      ordering_fields = "__all__"
      
      # This method should be overriden
      # if we dont want to modify query set based on current instance attributes
      def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

      def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
