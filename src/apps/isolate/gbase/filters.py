from .models import Genome, Mlst, Resistome, Virulome, Annotation
from gizmos.util import *
from django_filters import rest_framework as filters
from django_filters.constants import EMPTY_VALUES
from djongo import models
from rest_framework.compat import distinct
from rest_framework.filters import SearchFilter
import operator
from functools import reduce

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

class AttrFilter(Filter):
    # only for depth = 2
    
    def filter(self, qs, value):
        if value in EMPTY_VALUES:
            return qs
        hierarchy = self.field_name.split("__")
        print("*************************** attr")
        import json
        print(json.dumps(hierarchy))
        qs = qs.filter(attr={hierarchy[1]: value})
        print("*************************** after qs")
        from django.db import connection
        print(connection.queries) 
        
        return qs


class GenomeFilter(filters.FilterSet):
    
    owner__username = CharFilter(lookup_expr="iexact")
    sequence__Projectid = CharFilter(lookup_expr="iexact")
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
    
    id = CharFilter(lookup_expr="icontains")
    owner__username = CharFilter(lookup_expr="iexact")
    sequence__Projectid = CharFilter(lookup_expr='iexact')
    seqtype = CharFilter(lookup_expr="iexact")
    #allow the partial match
    scheme = CharFilter(lookup_expr="iexact")
    st = NumberFilter(lookup_expr="exact")
    DateCreated = DateFromToRangeFilter()
    LastUpdate = DateFromToRangeFilter()
    Description = CharFilter(lookup_expr="icontains")

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
            "sequence"
           
        )  # Temporary

class ResistomeFilter(filters.FilterSet):
    id = CharFilter(lookup_expr="icontains")
    owner__username = CharFilter(lookup_expr="iexact")
    sequence__Projectid = CharFilter(lookup_expr='iexact')
    seqtype = CharFilter(lookup_expr="iexact")
    #allow the partial match
    num_found = NumberFilter(lookup_expr="exact")
    DateCreated = DateFromToRangeFilter()
    LastUpdate = DateFromToRangeFilter()
    Description = CharFilter(lookup_expr="icontains")
    
    profile__geneName = ProfileFilter(
        field_name="profile__geneName", lookup_expr="iexact"
    )
    profile__pctCoverage = ProfileFilter(
        field_name="profile__pctCoverage", lookup_expr="exact"
    )

    class Meta:
        model = Resistome
        exclude = (
            "profile",
           
        )  # Temporary

class VirulomeFilter(filters.FilterSet):
    sequence__Projectid = CharFilter(lookup_expr="iexact")
    owner__username = CharFilter(lookup_expr="iexact")
    profile__geneName = ProfileFilter(
        field_name="profile__geneName", lookup_expr="icontain"
    )
    profile__pctCoverage = ProfileFilter(
        field_name="profile__pctCoverage", lookup_expr="exact"
    )

    class Meta:
        model = Virulome
        exclude = (
            "profile",
           
        )  # Temporary

class AnnotationFilter(filters.FilterSet):
    id = CharFilter(lookup_expr="icontains")
    owner__username = CharFilter(lookup_expr="iexact")
    sequence__Projectid = CharFilter(lookup_expr='iexact')
    seqtype = CharFilter(lookup_expr="iexact")
    
    seqid = CharFilter(lookup_expr="iexact")
    source = CharFilter(lookup_expr="iexact")
    ftype = CharFilter(lookup_expr="iexact")
    start = NumberFilter(lookup_expr="exact")
    end = NumberFilter(lookup_expr="exact")
    score = CharFilter(lookup_expr="iexact")
    strand = CharFilter(lookup_expr="iexact")
    phase = CharFilter(lookup_expr="iexact")

    DateCreated = DateFromToRangeFilter()
    LastUpdate = DateFromToRangeFilter()
    Description = CharFilter(lookup_expr="icontains")

    attr__tag = AttrFilter(
        field_name="attr__tag", lookup_expr="iexact"
    )
    attr__value = AttrFilter(
        field_name="attr__value", lookup_expr="iexact"
    )
    
    class Meta:
        model = Annotation
        exclude = (
            "attr",
            "sequence"
           
        )  # Temporary

class CustomSearchFilter(SearchFilter):

    def filter_queryset(self, request, queryset, view):
        nested_fields = [
            "profile__locus",
            "profile__allele"
        ]

        search_fields = self.get_search_fields(view, request)
        search_terms = self.get_search_terms(request)
        if not search_fields or not search_terms:
            return queryset

        nested_target = list(set(search_fields) & set(nested_fields))
        regular_target = list(set(search_fields) - set(nested_fields))

        orm_lookups = [
            self.construct_search(str(search_field))
            for search_field in regular_target
        ]

        nested_lookups = [
            self.construct_search(str(search_field))
            for search_field in nested_target
        ]

        conditions = []
        print("**************************************************************** search term")
        print(search_fields)
        print(orm_lookups)
        print(search_terms)
        for search_term in search_terms:
            queries = [
                models.Q(**{orm_lookup: search_term})
                for orm_lookup in orm_lookups
            ]
            conditions.append(reduce(operator.or_, queries))
        regular_queryset = queryset.filter(reduce(operator.and_, conditions))

        nested_conditions = []
        
        for search_term in search_terms:
            queries = [
                models.Q(
                    profile={
                        **{
                            # "__".join(
                            #     nested_lookup.split("__")[1:]
                            # ): search_term
                            nested_lookup.split("__")[1]: search_term
                            
                        }
                    }
                )
                
                for nested_lookup in nested_lookups
            ]
            nested_conditions.append(reduce(operator.or_, queries))
        nested_queryset = queryset.filter(
            reduce(operator.and_, nested_conditions)
        )

        queryset = regular_queryset | nested_queryset

        if self.must_call_distinct(queryset, search_fields):
            # Filtering against a many-to-many field requires us to
            # call queryset.distinct() in order to avoid duplicate items
            # in the resulting queryset.
            # We try to avoid this if possible, for performance reasons.
            queryset = distinct(queryset, base)
        return queryset


class AnnotationSearchFilter(SearchFilter):


    def filter_queryset(self, request, queryset, view):
        nested_fields = [
            "attr__tag",
            "attr__value"
        ]

        search_fields = self.get_search_fields(view, request)
        search_terms = self.get_search_terms(request)
        if not search_fields or not search_terms:
            return queryset

        nested_target = list(set(search_fields) & set(nested_fields))
        regular_target = list(set(search_fields) - set(nested_fields))

        orm_lookups = [
            self.construct_search(str(search_field))
            for search_field in regular_target
        ]

        nested_lookups = [
            self.construct_search(str(search_field))
            for search_field in nested_target
        ]

        conditions = []
        print("**************************************************************** search term")
        print(search_fields)
        print(orm_lookups)
        print(search_terms)

        for search_term in search_terms:
            print("search term=" + search_term)
            queries = [
                models.Q(**{orm_lookup: search_term})
                for orm_lookup in orm_lookups
            ]
            for orm_lookup in orm_lookups:
                print("asdfkas;dfjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj")
                print(type(orm_lookup))
                print(orm_lookup)
            if queries:
                conditions.append(reduce(operator.or_, queries))
        if conditions:
            regular_queryset = queryset.filter(reduce(operator.and_, conditions))
        else:
            regular_queryset = queryset

        nested_conditions = []
        
        for search_term in search_terms:
            queries = [
                models.Q(
                    attr={
                        **{
                            # "__".join(
                            #     nested_lookup.split("__")[1:]
                            # ): search_term
                            nested_lookup.split("__")[1]: search_term
                            
                        }
                    }
                )
                
                for nested_lookup in nested_lookups
            ]
            nested_conditions.append(reduce(operator.or_, queries))
        nested_queryset = queryset.filter(
            reduce(operator.and_, nested_conditions)
        )

        queryset = regular_queryset | nested_queryset

        if self.must_call_distinct(queryset, search_fields):
            # Filtering against a many-to-many field requires us to
            # call queryset.distinct() in order to avoid duplicate items
            # in the resulting queryset.
            # We try to avoid this if possible, for performance reasons.
            queryset = distinct(queryset, base)
        return queryset
        