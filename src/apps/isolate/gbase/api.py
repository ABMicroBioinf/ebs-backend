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
from .models import Assembly, Annotation, Virulome, Mlst, Resistome
from .filters import (
  AssemblyFilter,
  MlstFilter,
  MlstSearchFilter,
  ResistomeFilter,
  ResistomeSearchFilter,
  VirulomeFilter,
  VirulomeSearchFilter,
  AnnotationFilter,
  AnnotationSearchFilter
  
)

from .serializers import (
  AssemblySerializer, 
  AnnotationSerializer, 
  VirulomeSerializer, 
  MlstSerializer, 
  ResistomeSerializer
)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

class AssemblyViewSet(GenericViewSet,  # generic view functionality
                     CreateModelMixin,  # handles POSTs
                     RetrieveModelMixin,  # handles GETs for 1 Company
                     UpdateModelMixin,  # handles PUTs and PATCHes
                     ListModelMixin,  # handles GETs for many Companies
                     DestroyModelMixin,): #handle delete
      
      queryset = Assembly.objects.all()
      serializer_class = AssemblySerializer
      filterset_class = AssemblyFilter
      pagination_class = CustomPagination

      filter_backends = (
          SearchFilter,
          OrderingFilter,
          filters.DjangoFilterBackend,
      )

      search_fields = AssemblyFilter.Meta.fields
      ordering = ['DateCreated']

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
      queryset = Mlst.objects.all()
      serializer_class = MlstSerializer
      filterset_class = MlstFilter
      pagination_class = CustomPagination

      filter_backends = (
         # SearchFilter,
          MlstSearchFilter,
          OrderingFilter,
          filters.DjangoFilterBackend,
      )
    
      #filterset_fields define equaity based searching, this is defined in SequenceFilter class
      print("equaity based search fields: *******************************************")
      print(MlstFilter.Meta.fields)
      search_fields = MlstFilter.Meta.fields
      ordering = ['DateCreated']

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
      
      queryset = Resistome.objects.all()
      serializer_class = ResistomeSerializer
      filterset_class = ResistomeFilter
      pagination_class = CustomPagination
      filter_backends = (
          #SearchFilter,
          ResistomeSearchFilter,
          OrderingFilter,
          filters.DjangoFilterBackend,
      )
      #filterset_fields define equaity based searching, this is defined in SequenceFilter class
      print("equaity based search fields: *******************************************")
      print(ResistomeFilter.Meta.fields)
      search_fields = ResistomeFilter.Meta.fields
      ordering = ['DateCreated']
      
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

      queryset = Virulome.objects.all()
      serializer_class = VirulomeSerializer
      filterset_class = VirulomeFilter
      pagination_class = CustomPagination
      filter_backends = (
          #SearchFilter,
          VirulomeSearchFilter,
          OrderingFilter,
          filters.DjangoFilterBackend,
      )

      #filterset_fields define equaity based searching, this is defined in SequenceFilter class
      print("equaity based search fields: *******************************************")
      print(VirulomeFilter.Meta.fields)
      search_fields = VirulomeFilter.Meta.fields
      ordering = ['DateCreated']
      
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

      queryset = Annotation.objects.all()
      serializer_class = AnnotationSerializer
      filterset_class = AnnotationFilter
      pagination_class = CustomPagination
      filter_backends = (
          #SearchFilter,
          AnnotationSearchFilter,
          OrderingFilter,
          filters.DjangoFilterBackend,
      )

      #filterset_fields define equaity based searching, this is defined in SequenceFilter class
      print("equaity based search fields: *******************************************")
      print(AnnotationFilter.Meta.fields)
      search_fields = AnnotationFilter.Meta.fields
      ordering = ['DateCreated']
      
      # This method should be overriden
      # if we dont want to modify query set based on current instance attributes
      def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
   

      def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
