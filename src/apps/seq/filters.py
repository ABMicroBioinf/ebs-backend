from djongo import models
from django_filters import rest_framework 
from django_filters.filters import (
    CharFilter,
    DateFromToRangeFilter,
    Filter,
    NumberFilter,    
)
from rest_framework.filters import SearchFilter
from .models import (
    Sequence,
    BioSample,
)

from gizmos.filter import (
    EbsSearchFilter, 
    NestedFilter,
    MultipleCharValueFilter,
    EbsOrderingFilter
)
from typing import Tuple, List

class BioSampleFilter(rest_framework.FilterSet):
    
    project__id = MultipleCharValueFilter(lookup_expr="in")
    project__title = MultipleCharValueFilter(lookup_expr="icontains")
    DateCreated  = MultipleCharValueFilter(lookup_expr="in")
    LastUpdate = MultipleCharValueFilter(lookup_expr="in")
    

    class Meta:
        model = BioSample
        
        #equality-based filtering
        fields = [field.name for field in BioSample._meta.fields]
        # fields.remove("owner")
        # fields.remove("project")
        extra = [
            "project__id",
            "project__title",
            "owner__username",
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

class BioSampleSearchFilter(SearchFilter):
   
    class Meta:
        model = BioSample
        
        #equality-based filtering
        fields = [field.name for field in BioSample._meta.fields]
        # fields.remove("owner")
        # fields.remove("project")
        
        extra = [
           "project__id",
            "project__title",
            "owner__username"
        ]
        fields = fields + extra
        

#define equaity based filter
class SequenceFilter(rest_framework.FilterSet):
    
    project__id = MultipleCharValueFilter(lookup_expr="in")
    project__title = MultipleCharValueFilter(lookup_expr="icontains")
    
    biosample__id = MultipleCharValueFilter(lookup_expr="in")
    biosample__ScientificName = MultipleCharValueFilter(lookup_expr="icontains")
    
    Experiment = MultipleCharValueFilter(lookup_expr="in")
    LibraryName = MultipleCharValueFilter(lookup_expr="in")
    LibraryStrategy = MultipleCharValueFilter(lookup_expr="in")
    LibrarySelection = MultipleCharValueFilter(lookup_expr="in")
    LibrarySource = MultipleCharValueFilter(lookup_expr="in")
    LibraryLayout = MultipleCharValueFilter(lookup_expr="in")
    Platform = MultipleCharValueFilter(lookup_expr="in")
    SequencerModel = MultipleCharValueFilter(lookup_expr="in")
    CenterName = MultipleCharValueFilter(lookup_expr="in")
    sampleType = MultipleCharValueFilter(field_name ="sampleType", lookup_expr="in")
    DateCreated  = MultipleCharValueFilter(lookup_expr="in")
    LastUpdate = MultipleCharValueFilter(lookup_expr="in")
    

    class Meta:
        model = Sequence
        
        #equality-based filtering
        fields = [field.name for field in Sequence._meta.fields]
        # fields.remove("owner")
        # fields.remove("project")
        extra = [
            "project__id",
            "project__title",
            "biosample__id",
            "biosample__ScientificName",
            "owner__username",
            "seqstat__r_Reads",
             "seqstat__r_GeeCee",
             "seqstat__r_Yield",
             "seqstat__r_MinLen",
              "seqstat__r_AvgLen",
             "seqstat__r_MaxLen",
             "seqstat__r_AvgQual",
             "seqstat__r_ErrQual",
             "seqstat__r_Ambiguous",
              "seqstat__q_Reads",
             "seqstat__q_GeeCee",
             "seqstat__q_Yield",
             "seqstat__q_MinLen",
              "seqstat__q_AvgLen",
             "seqstat__q_MaxLen",
             "seqstat__q_AvgQual",
             "seqstat__q_ErrQual",
             "seqstat__q_Ambiguous"
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

class SequenceSearchFilter(SearchFilter):
   
    class Meta:
        model = Sequence
        
        #equality-based filtering
        fields = [field.name for field in Sequence._meta.fields]
        # fields.remove("owner")
        # fields.remove("project")
        
        extra = [
           "project__id",
            "project__title",
            "biosample__id",
            "biosample__ScientificName",
            "owner__username"
        ]
        fields = fields + extra
        

