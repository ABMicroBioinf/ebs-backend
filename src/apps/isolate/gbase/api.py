from rest_framework.mixins import (
    CreateModelMixin, 
    ListModelMixin, 
    RetrieveModelMixin, 
    UpdateModelMixin, 
    DestroyModelMixin
)
from rest_framework.viewsets import GenericViewSet
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters import rest_framework as filters
from gizmos.pagination import CustomPagination
from .models import Genome, Annotation, Virulome, Mlst, Resistome
from .filters import GenomeFilter, MlstFilter, ResistomeFilter, VirulomeFilter

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
      filterset_class = GenomeFilter
      pagination_class = CustomPagination
      filter_backends = (
          SearchFilter,
          OrderingFilter,
          filters.DjangoFilterBackend,
      )
      # __all__ not working with the API search box on browser
      search_fields = [
        'bp',
        'Ns',
        'gaps',
        'min',
        'avg',
        'max',
        'N50',
        'count',
        'id',
        'seqtype',
        'owner__username',
        'DateCreated',
        'LastUpdate',
        'Description',

      ]
      ordering_fields = [
        'bp',
        'Ns',
        'gaps',
        'min',
        'avg',
        'max',
        'N50',
        'count',
        'id',
        'seqtype',
        'owner__username',
        'DateCreated',
        'LastUpdate',
      ]

      # This method should be overriden
      # if we dont want to modify query set based on current instance attributes
      def get_queryset(self):
        return Genome.objects.filter(owner=self.request.user)

      
      def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class MlstViewSet(GenericViewSet,  # generic view functionality
                     CreateModelMixin,  # handles POSTs
                     RetrieveModelMixin,  # handles GETs for 1 Company
                     UpdateModelMixin,  # handles PUTs and PATCHes
                     ListModelMixin,  # handles GETs for many Companies
                     DestroyModelMixin,): #handle delete

      serializer_class = MlstSerializer
      filterset_class = MlstFilter
      pagination_class = CustomPagination
      filter_backends = (
          SearchFilter,
          OrderingFilter,
          filters.DjangoFilterBackend,
      )
      # search_fields = "__all__"
      # ordering_fields = "__all__"
      search_fields = [
        "id",
        "owner__username",
        "seqtype",
        "scheme",
        "st",
        "DateCreated",
        "LastUpdate", 
        "Description"
        ]
      ordering_fields =  [
        "id",
        "owner__username",
        "seqtype",
        "scheme",
        "st",
        "DateCreated",
        "LastUpdate", 
        ]
      
      # This method should be overriden
      # if we dont want to modify query set based on current instance attributes
      def get_queryset(self):
        return Mlst.objects.filter(owner=self.request.user)

      def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ResistomeViewSet(GenericViewSet,  # generic view functionality
                     CreateModelMixin,  # handles POSTs
                     RetrieveModelMixin,  # handles GETs for 1 Company
                     UpdateModelMixin,  # handles PUTs and PATCHes
                     ListModelMixin,  # handles GETs for many Companies
                     DestroyModelMixin,): #handle delete

      serializer_class = ResistomeSerializer
      filterset_class = ResistomeFilter
      pagination_class = CustomPagination
      filter_backends = (
          SearchFilter,
          OrderingFilter,
          filters.DjangoFilterBackend,
      )
      search_fields = [
        "id",
        "owner__username",
        "seqtype",
        "num_found",
        "DateCreated",
        "LastUpdate", 
        "Description"
        ]
      ordering_fields = [
        "id",
        "owner__username",
        "seqtype",
        "num_found",
        "DateCreated",
        "LastUpdate", 
        
        ]
      queryset = Resistome.objects.all()
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
      filterset_class = VirulomeFilter
      pagination_class = CustomPagination
      filter_backends = (
          SearchFilter,
          OrderingFilter,
          filters.DjangoFilterBackend,
      )
      search_fields = [
        "id",
        "owner__username",
        "seqtype",
        "num_found",
        "DateCreated",
        "LastUpdate", 
        "Description"
        ]
      ordering_fields = [
        "id",
        "owner__username",
        "seqtype",
        "num_found",
        "DateCreated",
        "LastUpdate", 
        
        ]
      queryset = Virulome.objects.all()
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
      #pagination_class.page_size = 1
      filter_backends = (SearchFilter, OrderingFilter)
      search_fields = "__all__"
      ordering_fields = "__all__"
      
      # This method should be overriden
      # if we dont want to modify query set based on current instance attributes
      def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

      def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
