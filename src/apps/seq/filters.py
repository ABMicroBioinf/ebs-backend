from djongo import models
from django_filters import rest_framework 
from django_filters.filters import (
    CharFilter,
    DateFromToRangeFilter,
    Filter,
    NumberFilter,    
)
from .models import Sequence
from gizmos.filter import EbsSearchFilter, NestedFilter

#define equaity based filter
class SequenceFilter(rest_framework.FilterSet):
    
    RawStats__Reads = NestedFilter(
        field_name="RawStats__Reads", lookup_expr="exact"
    )
    RawStats__Yield = NestedFilter(
        field_name="RawStats__Yield", lookup_expr="exact"
    )
    RawStats__GeeCee = NestedFilter(
        field_name="RawStats__GeeCee", lookup_expr="exact"
    )
    RawStats__MinLen = NestedFilter(
        field_name="RawStats__MinLen", lookup_expr="exact"
    )
    RawStats__AvgLen = NestedFilter(
        field_name="RawStats__AvgLen", lookup_expr="exact"
    )
    RawStats__MaxLen = NestedFilter(
        field_name="RawStats__MaxLen", lookup_expr="exact"
    )
    RawStats__AvgQual = NestedFilter(
        field_name="RawStats__AvgQual", lookup_expr="exact"
    )
    RawStats__ErrQual = NestedFilter(
        field_name="RawStats__ErrQual", lookup_expr="exact"
    )
    RawStats__Ambiguous = NestedFilter(
        field_name="RawStats__Ambiguous", lookup_expr="exact"
    )

    QcStats__Reads = NestedFilter(
        field_name="QcStats__Reads", lookup_expr="exact"
    )
    QcStats__Yield = NestedFilter(
        field_name="QcStats__Yield", lookup_expr="exact"
    )
    QcStats__GeeCee = NestedFilter(
        field_name="QcStats__GeeCee", lookup_expr="exact"
    )
    QcStats__MinLen = NestedFilter(
        field_name="QcStats__MinLen", lookup_expr="exact"
    )
    QcStats__AvgLen = NestedFilter(
        field_name="QcStats__AvgLen", lookup_expr="exact"
    )
    QcStats__MaxLen = NestedFilter(
        field_name="QcStats__MaxLen", lookup_expr="exact"
    )
    QcStats__AvgQual = NestedFilter(
        field_name="QcStats__AvgQual", lookup_expr="exact"
    )
    QcStats__ErrQual = NestedFilter(
        field_name="QcStats__ErrQual", lookup_expr="exact"
    )
    QcStats__Ambiguous = NestedFilter(
        field_name="QcStats__Ambiguous", lookup_expr="exact"
    )
    
    class Meta:
        model = Sequence
        
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
                'filter_class': CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
            models.IntegerField: {
                'filter_class': NumberFilter,
                'extra': lambda f: {
                    'lookup_expr': 'exact',
                },
            },
        }

class SequenceSearchFilter(EbsSearchFilter):
    def __init__(self):
        self.nested_fields =  [
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
        self.nested_cats = [
            'RawStats',
            'QcStats',
           
        ]
