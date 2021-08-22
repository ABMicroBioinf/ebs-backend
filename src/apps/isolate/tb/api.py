from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
)
from rest_framework.viewsets import GenericViewSet
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters import rest_framework as filters
from .models import Profile, Psummary
from .serializers import ProfileSerializer, PsummarySerializer
from gizmos.pagination import CustomPagination
from .filters import ProfileFilter, PsummaryFilter

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
          SearchFilter,
          #CustomSearchFilter,
          OrderingFilter,
          filters.DjangoFilterBackend,
      )
      search_fields = "__all__"
      ordering_fields = "__all__"
      
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
          #CustomSearchFilter,
          OrderingFilter,
          filters.DjangoFilterBackend,
      )
      
      ordering_fields = "__all__"
      search_fields = [

        "id",
        "sequence__Projectid",
        "owner__username",
        "Description",
        "DateCreated",
        "LastUpdate",
        "pct_reads_mapped",
        "num_reads_mapped",
        "main_lin",
        "sublin",
        "num_dr_variants",
        "num_other_variants",
        "drtype",
        "rifampicin",
        "isoniazid",
        "pyrazinamide",
        "ethambutol",
        "streptomycin",
        "fluoroquinolones",
        "moxifloxacin",
        "ofloxacin",
        "levofloxacin",
        "ciprofloxacin",
        "aminoglycosides",
        "amikacin",
        "kanamycin",
        "capreomycin",
        "ethionamide",
        "para_aminosalicylic_acid",
        "cycloserine",
        "linezolid",
        "bedaquiline",
        "clofazimine",
        "delamanid",
        "sequence"

      ]
      
      # This method should be overriden
      # if we dont want to modify query set based on current instance attributes
      def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

      def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
