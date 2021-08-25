from .models import Sequence
from gizmos.util import *
from django_filters import rest_framework as filters
from django_filters.constants import EMPTY_VALUES
from djongo import models
from rest_framework.compat import distinct
from rest_framework.filters import SearchFilter
import operator
from functools import reduce
from djongo import models
import django_filters

from django_filters.filters import (
    CharFilter,
    DateFromToRangeFilter,
    Filter,
    NumberFilter,
    
)

class RawStatsFilter(Filter):
    # only for depth = 2
    
    def filter(self, qs, value):
        if value in EMPTY_VALUES:
            return qs
        hierarchy = self.field_name.split("__")
        qs = qs.filter(RawStats={hierarchy[1]: num(value)})
        """ from django.db import connection
        print(connection.queries) """
        
        return qs


class QcStatsFilter(Filter):
    # only for depth = 2
    def filter(self, qs, value):
        if value in EMPTY_VALUES:
            return qs
        hierarchy = self.field_name.split("__")
        qs = qs.filter(QcStats={hierarchy[1]: num(value)})
        return qs

class MultipleCharValueFilter(Filter):
    def filter(self, qs, value):
        if value in EMPTY_VALUES:
            return qs
        value_list = value.split(",")
        qs = super().filter(qs, value_list)
        return qs

#define equaity based filter
class SequenceFilter(filters.FilterSet):
    
    RawStats__Reads = RawStatsFilter(
        field_name="RawStats__Reads", lookup_expr="exact"
    )
    RawStats__Yield = RawStatsFilter(
        field_name="RawStats__Yield", lookup_expr="exact"
    )
    RawStats__GeeCee = RawStatsFilter(
        field_name="RawStats__GeeCee", lookup_expr="exact"
    )
    RawStats__MinLen = RawStatsFilter(
        field_name="RawStats__MinLen", lookup_expr="exact"
    )
    RawStats__AvgLen = RawStatsFilter(
        field_name="RawStats__AvgLen", lookup_expr="exact"
    )
    RawStats__MaxLen = RawStatsFilter(
        field_name="RawStats__MaxLen", lookup_expr="exact"
    )
    RawStats__AvgQual = RawStatsFilter(
        field_name="RawStats__AvgQual", lookup_expr="exact"
    )
    RawStats__ErrQual = RawStatsFilter(
        field_name="RawStats__ErrQual", lookup_expr="exact"
    )
    RawStats__Ambiguous = RawStatsFilter(
        field_name="RawStats__Ambiguous", lookup_expr="exact"
    )

    QcStats__Reads = QcStatsFilter(
        field_name="QcStats__Reads", lookup_expr="exact"
    )
    QcStats__Yield = QcStatsFilter(
        field_name="QcStats__Yield", lookup_expr="exact"
    )
    QcStats__GeeCee = QcStatsFilter(
        field_name="QcStats__GeeCee", lookup_expr="exact"
    )
    QcStats__MinLen = QcStatsFilter(
        field_name="QcStats__MinLen", lookup_expr="exact"
    )
    QcStats__AvgLen = QcStatsFilter(
        field_name="QcStats__AvgLen", lookup_expr="exact"
    )
    QcStats__MaxLen = QcStatsFilter(
        field_name="QcStats__MaxLen", lookup_expr="exact"
    )
    QcStats__AvgQual = QcStatsFilter(
        field_name="QcStats__AvgQual", lookup_expr="exact"
    )
    QcStats__ErrQual = QcStatsFilter(
        field_name="QcStats__ErrQual", lookup_expr="exact"
    )
    QcStats__Ambiguous = QcStatsFilter(
        field_name="QcStats__Ambiguous", lookup_expr="exact"
    )
    
    class Meta:
        model = Sequence
        """ exclude = (
            "RawStats",
            "QcStats",
        )  # Temporary """
        #equality-based filtering
        fields = [field.name for field in Sequence._meta.fields]
        fields.remove("owner")
        fields.remove("project")
        fields.remove("QcStats")
        fields.remove("RawStats")
        extra = [
            "RawStats__Reads",
            "RawStats__Yield",
            "RawStats__GeeCee",
            "RawStats__MinLen",
            "RawStats__AvgLen",
            "RawStats__MaxLen",
            "RawStats__AvgQual",
            "RawStats__ErrQual",
            "RawStats__Ambiguous",
            "QcStats__Reads",
            "QcStats__Yield",
            "QcStats__GeeCee",
            "QcStats__MinLen",
            "QcStats__AvgLen",
            "QcStats__MaxLen",
            "QcStats__AvgQual",
            "QcStats__ErrQual",
            "QcStats__Ambiguous",
            "project__id",
            "project__title",
            "owner__username"
        ]
        fields = fields + extra
        
        #it is possible to override default filters for all the models fields of the same kind using filter_overrides on the Meta class:
        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
            models.IntegerField: {
                'filter_class': django_filters.NumberFilter,
                'extra': lambda f: {
                    'lookup_expr': 'exact',
                },
            },
        }

class CustomSearchFilter(SearchFilter):
    def filter_queryset(self, request, queryset, view):
        nested_fields = [
            "RawStats__Reads",
            "RawStats__Yield",
            "RawStats__GeeCee",
            "RawStats__MinLen",
            "RawStats__AvgLen",
            "RawStats__MaxLen",
            "RawStats__AvgQual",
            "RawStats__ErrQual",
            "RawStats__Ambiguous",
            "QcStats__Reads",
            "QcStats__Yield",
            "QcStats__GeeCee",
            "QcStats__MinLen",
            "QcStats__AvgLen",
            "QcStats__MaxLen",
            "QcStats__AvgQual",
            "QcStats__ErrQual",
            "QcStats__Ambiguous",
        ]

        search_fields = self.get_search_fields(view, request)
        search_terms = self.get_search_terms(request)
        print("*********************************")
        print(type(search_fields))
        print(search_fields)
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

        base = queryset

        conditions = []
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
                    RawStats={
                        **{
                            # "__".join(
                            #     nested_lookup.split("__")[1:]
                            # ): search_term
                            nested_lookup.split("__")[1]: search_term
                        }
                    }
                )
                if nested_lookup.split("__")[0] == "RawStats"
                else models.Q(
                    QcStats={
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
