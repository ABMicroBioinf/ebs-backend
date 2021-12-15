from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response

from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
)
from rest_framework.viewsets import GenericViewSet

from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters import rest_framework as filters
from .models import Profile, Psummary
from .serializers import ProfileSerializer, PsummarySerializer, PsummaryMetadataSerializer
from gizmos.pagination import CustomPagination
from .filters import ProfileFilter, PsummaryFilter, ProfileSearchFilter

class ProfileViewSet(GenericViewSet,  # generic view functionality
                     CreateModelMixin,  # handles POSTs
                     RetrieveModelMixin,  # handles GETs for 1 Company
                     UpdateModelMixin,  # handles PUTs and PATCHes
                     ListModelMixin,  # handles GETs for many Companies
                     DestroyModelMixin,): #handle delete

      queryset = Profile.objects.all()
      serializer_class = ProfileSerializer
      filterset_class = ProfileFilter
      pagination_class = CustomPagination
      filter_backends = (
          #SearchFilter,
          ProfileSearchFilter,
          OrderingFilter,
          filters.DjangoFilterBackend,
      )
      #filterset_fields define equaity based searching, this is defined in SequenceFilter class
      print("equaity based search fields: *******************************************")
      print(ProfileFilter.Meta.fields)
      search_fields = ProfileFilter.Meta.fields
      ordering = ['DateCreated']

      # This method should be overriden
      # if we dont want to modify query set based on current instance attributes
      def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

      def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PsummaryViewSet(GenericViewSet,  # generic view functionality
                     CreateModelMixin,  # handles POSTs
                     RetrieveModelMixin,  # handles GETs for 1 Company
                     UpdateModelMixin,  # handles PUTs and PATCHes
                     ListModelMixin,  # handles GETs for many Companies
                     DestroyModelMixin,): #handle delete

      queryset = Psummary.objects.all()
      serializer_class = PsummarySerializer
      filterset_class = PsummaryFilter
      pagination_class = CustomPagination
      filter_backends = (
          SearchFilter,
          OrderingFilter,
          filters.DjangoFilterBackend,
      )
      
      #filterset_fields define equaity based searching, this is defined in SequenceFilter class
      print("equaity based search fields: *******************************************")
      print(PsummaryFilter.Meta.fields)
      search_fields = PsummaryFilter.Meta.fields
      ordering = ['DateCreated']

      # This method should be overriden
      # if we dont want to modify query set based on current instance attributes
      def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

      def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        
      @action(detail=False)
      def metadata(self, request):
        psummary = Psummary.objects.all()
        serializer = PsummaryMetadataSerializer(psummary)
        return Response(serializer.data, status=status.HTTP_200_OK)
