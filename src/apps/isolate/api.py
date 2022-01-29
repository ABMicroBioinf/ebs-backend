from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response

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
from .models import Assembly, Stats, Annotation, Virulome, Mlst, Resistome
from .filters import (
  AssemblyFilter,
  StatsFilter,
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
  AssemblyMetadataSerializer,
  StatsSerializer,
  StatsMetadataSerializer,
  AnnotationSerializer, 
  VirulomeSerializer,
  VirulomeMetadataSerializer,
  MlstSerializer,
  MlstMetadataSerializer,
  ResistomeSerializer,
  ResistomeMetadataSerializer
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
        
      @action(detail = False)
      def metadata(self, request):
        
        assembly = (
          Assembly.objects.filter(seqtype = request.query_params["seqtype"])
          if "seqtype" in request.GET
          else Assembly.objects.all()
        )
        #seqtype = request.query_params["seqtype"]
        #assembly = Assembly.objects.filter(seqtype=seqtype)
        serializer = AssemblyMetadataSerializer(assembly)
        return Response(serializer.data, status=status.HTTP_200_OK)
      
class StatsViewSet(GenericViewSet,  # generic view functionality
                     CreateModelMixin,  # handles POSTs
                     RetrieveModelMixin,  # handles GETs for 1 Company
                     UpdateModelMixin,  # handles PUTs and PATCHes
                     ListModelMixin,  # handles GETs for many Companies
                     DestroyModelMixin,): #handle delete
      
      queryset = Stats.objects.all()
      serializer_class = StatsSerializer
      filterset_class = StatsFilter
      pagination_class = CustomPagination

      filter_backends = (
          SearchFilter,
          OrderingFilter,
          filters.DjangoFilterBackend,
      )

      search_fields = StatsFilter.Meta.fields
      ordering = ['DateCreated']

      # This method should be overriden
      # if we dont want to modify query set based on current instance attributes
      def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

      
      def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        
      @action(detail = False)
      def metadata(self, request):
        stats = (
          Stats.objects.filter(seqtype = request.query_params["seqtype"])
          if "seqtype" in request.GET
          else Stats.objects.all()
        )
        serializer = StatsMetadataSerializer(stats)
        return Response(serializer.data, status=status.HTTP_200_OK)
      
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
        print(self.queryset)
        return self.queryset.filter(owner=self.request.user)

      def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
      
      @action(detail = False)
      def metadata(self, request):
        mlst = (
          Mlst.objects.filter(seqtype = request.query_params["seqtype"])
          if "seqtype" in request.GET
          else Mlst.objects.all()
        )
        serializer = MlstMetadataSerializer(mlst)
        return Response(serializer.data, status=status.HTTP_200_OK)

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

      @action(detail = False)
      def metadata(self, request):
        resistome = (
          Resistome.objects.filter(seqtype = request.query_params["seqtype"])
          if "seqtype" in request.GET
          else Resistome.objects.all()
        )
        serializer = ResistomeMetadataSerializer(resistome)
        return Response(serializer.data, status=status.HTTP_200_OK)


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

      @action(detail = False)
      def metadata(self, request):
        virulome = (
          Virulome.objects.filter(seqtype = request.query_params["seqtype"])
          if "seqtype" in request.GET
          else Virulome.objects.all()
        )
        serializer = VirulomeMetadataSerializer(virulome)
        return Response(serializer.data, status=status.HTTP_200_OK)
      
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



from .models import TbProfile, TbProfileSummary
from .serializers import TbProfileSerializer, TbProfileSummarySerializer, TbProfileSummaryMetadataSerializer
from gizmos.pagination import CustomPagination
from .filters import TbProfileFilter, TbProfileSummaryFilter, TbProfileSearchFilter

class TbProfileViewSet(GenericViewSet,  # generic view functionality
                     CreateModelMixin,  # handles POSTs
                     RetrieveModelMixin,  # handles GETs for 1 Company
                     UpdateModelMixin,  # handles PUTs and PATCHes
                     ListModelMixin,  # handles GETs for many Companies
                     DestroyModelMixin,): #handle delete

      queryset = TbProfile.objects.all()
      serializer_class = TbProfileSerializer
      filterset_class = TbProfileFilter
      pagination_class = CustomPagination
      filter_backends = (
          #SearchFilter,
          TbProfileSearchFilter,
          OrderingFilter,
          filters.DjangoFilterBackend,
      )
      #filterset_fields define equaity based searching, this is defined in SequenceFilter class
      print("equaity based search fields: *******************************************")
      print(TbProfileFilter.Meta.fields)
      search_fields = TbProfileFilter.Meta.fields
      ordering = ['DateCreated']

      # This method should be overriden
      # if we dont want to modify query set based on current instance attributes
      def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

      def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TbProfileSummaryViewSet(GenericViewSet,  # generic view functionality
                     CreateModelMixin,  # handles POSTs
                     RetrieveModelMixin,  # handles GETs for 1 Company
                     UpdateModelMixin,  # handles PUTs and PATCHes
                     ListModelMixin,  # handles GETs for many Companies
                     DestroyModelMixin,): #handle delete

      queryset = TbProfileSummary.objects.all()
      serializer_class = TbProfileSummarySerializer
      filterset_class = TbProfileSummaryFilter
      pagination_class = CustomPagination
      filter_backends = (
          SearchFilter,
          OrderingFilter,
          filters.DjangoFilterBackend,
      )
      
      #filterset_fields define equaity based searching, this is defined in SequenceFilter class
      print("equaity based search fields: *******************************************")
      print(TbProfileSummaryFilter.Meta.fields)
      search_fields = TbProfileSummaryFilter.Meta.fields
      ordering = ['DateCreated']

      # This method should be overriden
      # if we dont want to modify query set based on current instance attributes
      def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

      def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        
      @action(detail=False)
      def metadata(self, request):
        psummary = TbProfileSummary.objects.all()
        serializer = TbProfileSummaryMetadataSerializer(psummary)
        return Response(serializer.data, status=status.HTTP_200_OK)