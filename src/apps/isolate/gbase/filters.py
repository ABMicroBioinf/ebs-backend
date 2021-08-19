from .models import Genome, Mlst, Resistome, Virulome
from gizmos.util import *
from django_filters import rest_framework as filters
from django_filters.constants import EMPTY_VALUES

from django_filters.filters import (
    CharFilter,
    DateFromToRangeFilter,
    Filter,
    NumberFilter,
)

class ProfileFilter(Filter):
    # only for depth = 2
    
    def filter(self, qs, value):
        if value in EMPTY_VALUES:
            return qs
        hierarchy = self.field_name.split("__")
        print("***************************")
        import json
        print(json.dumps(hierarchy))
        qs = qs.filter(profile={hierarchy[1]: value})
        print("*************************** after qs")
        from django.db import connection
        print(connection.queries) 
        
        return qs

class GenomeFilter(filters.FilterSet):
    
    owner = CharFilter(lookup_expr="iexact")
    seqtype = CharFilter(lookup_expr="iexact")
    #allow the partial match
    id = CharFilter(lookup_expr="icontains")
    count = NumberFilter(lookup_expr="exact")
    bp = NumberFilter(lookup_expr="exact")
    Ns = NumberFilter(lookup_expr="exact")
    gaps = NumberFilter(lookup_expr="exact")
    min = NumberFilter(lookup_expr="exact")
    max = NumberFilter(lookup_expr="exact")
    avg = NumberFilter(lookup_expr="exact")
    N50 = NumberFilter(lookup_expr="exact")

class MlstFilter(filters.FilterSet):
    
    # id = CharFilter(lookup_expr="icontains")
    # owner = CharFilter(lookup_expr="iexact")
    # seqtype = CharFilter(lookup_expr="iexact")
    # #allow the partial match
    # scheme = CharFilter(lookup_expr="iexact")
    #st = NumberFilter(lookup_expr="exact")
    # DateCreated = DateFromToRangeFilter()
    # LastUpdate = DateFromToRangeFilter()
    # Description = CharFilter(lookup_expr="icontains")

    profile__locus = ProfileFilter(
        field_name="profile__locus", lookup_expr="icontains"
    )
    profile__allele = ProfileFilter(
        field_name="profile__allele", lookup_expr="iexact"
    )

    class Meta:
        model = Mlst
        exclude = (
            "profile",
           
        )  # Temporary

class ResistomeFilter(filters.FilterSet):
    
    profile__geneName = ProfileFilter(
        field_name="profile__geneName", lookup_expr="icontain"
    )
    profile__pct_coverage = ProfileFilter(
        field_name="profile__pct_coverage", lookup_expr="exact"
    )

    class Meta:
        model = Resistome
        exclude = (
            "profile",
           
        )  # Temporary

class VirulomeFilter(filters.FilterSet):
    
    profile__geneName = ProfileFilter(
        field_name="profile__geneName", lookup_expr="icontain"
    )
    profile__pct_coverage = ProfileFilter(
        field_name="profile__pct_coverage", lookup_expr="exact"
    )

    class Meta:
        model = Virulome
        exclude = (
            "profile",
           
        )  # Temporary
        