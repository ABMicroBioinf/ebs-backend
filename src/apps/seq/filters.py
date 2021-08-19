from .models import Sequence
from gizmos.util import *
from django_filters import rest_framework as filters
from django_filters.constants import EMPTY_VALUES

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
        qs = qs.filter(QcStats={hierarchy[1]: value})
        return qs


class MultipleCharValueFilter(Filter):
    def filter(self, qs, value):
        if value in EMPTY_VALUES:
            return qs
        value_list = value.split(",")
        qs = super().filter(qs, value_list)
        return qs


class SequenceFilter(filters.FilterSet):
    
    owner = CharFilter(lookup_expr="iexact")
    seqtype = CharFilter(lookup_expr="iexact")

    id = CharFilter(lookup_expr="icontains")
    #default lookup_expr is exact
    TaxID = NumberFilter(lookup_expr="exact")
    
    ScientificName = CharFilter(lookup_expr="icontains")
    Experiment = MultipleCharValueFilter(lookup_expr="in")
    LibraryName = MultipleCharValueFilter(lookup_expr="in")
    LibraryStrategy = MultipleCharValueFilter(lookup_expr="in")
    LibrarySelection = MultipleCharValueFilter(lookup_expr="in")
    LibrarySource = MultipleCharValueFilter(lookup_expr="in")
    LibraryLayout = MultipleCharValueFilter(lookup_expr="in")
    Platform = MultipleCharValueFilter(lookup_expr="in")
    SequencerModel = MultipleCharValueFilter(lookup_expr="in")
    Projectid = MultipleCharValueFilter(lookup_expr="in")
    SampleName = CharFilter(lookup_expr="icontains")
    CenterName = MultipleCharValueFilter(lookup_expr="in")
    DateCreated = DateFromToRangeFilter()
    LastUpdate = DateFromToRangeFilter()
    Description = CharFilter(lookup_expr="icontains")

    taxName_1 = CharFilter(lookup_expr="icontains")
    taxFrac_1 = NumberFilter(lookup_expr="exact")
    taxName_2 = CharFilter(lookup_expr="icontains")
    taxFrac_2 = NumberFilter(lookup_expr="exact")
    taxName_3 = CharFilter(lookup_expr="icontains")
    taxFrac_3 = NumberFilter(lookup_expr="exact")
    taxName_4 = CharFilter(lookup_expr="icontains")
    taxFrac_4 = NumberFilter(lookup_expr="exact")

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
        exclude = (
            "InsertSize",
            "InsertDev",
            "RawStats",
            "QcStats",
        )  # Temporary
        
        