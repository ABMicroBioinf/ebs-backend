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
  ResistomeFilter, 
  VirulomeFilter, 
  CustomSearchFilter,
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
          #SearchFilter,
          CustomSearchFilter,
          OrderingFilter,
          filters.DjangoFilterBackend,
      )
      

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
      filterset_class = ResistomeFilter
      pagination_class = CustomPagination
      filter_backends = (
          #SearchFilter,
          CustomSearchFilter,
          OrderingFilter,
          filters.DjangoFilterBackend,
      )
      search_fields = [
        "id",
        'sequence__Projectid',
        "owner__username",
        "seqtype",
        "num_found",
        "DateCreated",
        "LastUpdate", 
        "Description",
        "profile__geneName",
        "profile__pctCoverage"
        ]
      ordering_fields = [
        "id",
        'sequence__Projectid',
        "owner__username",
        "seqtype",
        "num_found",
        "DateCreated",
        "LastUpdate",
        "profile__geneName",
        "profile__pctCoverage"
        
        ]
      queryset = Resistome.objects.all()

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
          #SearchFilter,
          CustomSearchFilter,
          OrderingFilter,
          filters.DjangoFilterBackend,
      )
      search_fields = [
        "id",
        'sequence__Projectid',
        "owner__username",
        "seqtype",
        "num_found",
        "DateCreated",
        "LastUpdate", 
        "Description",
        "profile__geneName",
        "profile__pctCoverage"
        ]
      ordering_fields = [
        "id",
        'sequence__Projectid',
        "owner__username",
        "seqtype",
        "num_found",
        "DateCreated",
        "LastUpdate", 
        "profile__geneName",
        "profile__pctCoverage"
        
        ]
      queryset = Virulome.objects.all()
     

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
      # search_fields = "__all__"
      # ordering_fields = "__all__"

      search_fields = [
        'id',
        'owner__username',
        'sequence__Projectid',
        'seqid',
        'ftype',
        'start',
        'end',
        'seqtype',
        'DateCreated',
        'LastUpdate', 
        'Description',
        'sequence_id',
        'attr__tag',
        'attr__value'
      ]
      ordering_fields = [
        'id',
        'owner__username',
        'sequence__Projectid',
        'seqid',
        'ftype',
        'start',
        'end',
        'seqtype',
        'DateCreated',
        'LastUpdate', 
        'Description',
        'sequence_id',
        'attr__tag',
        'attr__value'
      ] 
   

      def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
