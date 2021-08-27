from djongo import models
from django_filters import rest_framework
from django_filters.filters import (
    CharFilter,
    DateFromToRangeFilter,
    Filter,
    NumberFilter,
) 
from .models import Psummary, Profile
from gizmos.filter import EbsSearchFilter, NestedFilter

class PsummaryFilter(rest_framework.FilterSet): 
   class Meta:
        model = Psummary
        
        #equality-based filtering
        fields = [field.name for field in Psummary._meta.fields]
        fields.remove("owner")
        fields.remove("sequence")
    
        extra = [
            "sequence__project__id",
            "sequence__project__title",
            "owner__username",
            "sequence__LibrarySource",
            "sequence__LibraryLayout",
            "sequence__SequencerModel",
            "sequence__CenterName",
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

class ProfileFilter(rest_framework.FilterSet): 
    
    lineage__lin = NestedFilter(
        field_name="lineage__lin", lookup_expr="iexact"
    )
    lineage__family = NestedFilter(
        field_name="lineage__family", lookup_expr="iexact"
    )
    lineage__spoligotype = NestedFilter(
        field_name="lineage__spoligotype", lookup_expr="iexact"
    )
    lineage__rd = NestedFilter(
        field_name="lineage__rd", lookup_expr="iexact"
    )
    lineage__frac = NestedFilter(
        field_name="lineage__frac", lookup_expr="exact"
    )

    dr_variants__chr = NestedFilter(
        field_name="dr_variants__chr", lookup_expr="iexact"
    )
    dr_variants__genome_pos = NestedFilter(
        field_name="dr_variants__genome_pos", lookup_expr="exact"
    )
    dr_variants__type = NestedFilter(
        field_name="dr_variants__type", lookup_expr="iexact"
    )
    dr_variants__change = NestedFilter(
        field_name="dr_variants__change", lookup_expr="iexact"
    )
    dr_variants__freq = NestedFilter(
        field_name="dr_variants__freq", lookup_expr="exact"
    )
    dr_variants__nucleotide_change = NestedFilter(
        field_name="dr_variants__nucleotide_change", lookup_expr="iexact"
    )
    dr_variants__locus_tag = NestedFilter(
        field_name="dr_variants__locus_tag", lookup_expr="iexact"
    )
    dr_variants__gene = NestedFilter(
        field_name="dr_variants__gene", lookup_expr="iexact"
    )
    dr_variants___internal_change = NestedFilter(
        field_name="dr_variants___internal_change ", lookup_expr="iexact"
    ) 
    other_variants__chr = NestedFilter(
        field_name="other_variants__chr", lookup_expr="iexact"
    )
    other_variants__genome_pos = NestedFilter(
        field_name="other_variants__genome_pos", lookup_expr="exact"
    )
    other_variants__type = NestedFilter(
        field_name="other_variants__type", lookup_expr="iexact"
    )
    other_variants__change = NestedFilter(
        field_name="other_variants__change", lookup_expr="iexact"
    )
    other_variants__freq = NestedFilter(
        field_name="other_variants__freq", lookup_expr="exact"
    )
    other_variants__nucleotide_change = NestedFilter(
        field_name="other_variants__nucleotide_change", lookup_expr="iexact"
    )
    other_variants__locus_tag = NestedFilter(
        field_name="other_variants__locus_tag", lookup_expr="iexact"
    )
    other_variants__gene = NestedFilter(
        field_name="other_variants__gene", lookup_expr="iexact"
    )
    other_variants___internal_change = NestedFilter(
        field_name="other_variants___internal_change", lookup_expr="iexact"
    )

    dr_resistances__drug = NestedFilter(
        field_name="dr_resistance__drug", lookup_expr="iexact"
    )
    dr_resistances__mutations = NestedFilter(
        field_name="dr_resistance__mutations", lookup_expr="iexact"
    )

    class Meta:
        model = Profile
        
        #equality-based filtering
        fields = [field.name for field in Profile._meta.fields]
        print(fields)
        fields.remove("owner")
        fields.remove("sequence")
        fields.remove("lineage")
        fields.remove("dr_variants")
        fields.remove("other_variants")
        fields.remove("dr_resistances")

        extra = [
            "lineage__lin",
            "lineage__family",
            "lineage__spoligotype",
            "lineage__rd",
            "lineage__frac",
            "dr_variants__chr",
            "dr_variants__genome_pos",
            "dr_variants__type",
            "dr_variants__change",
            "dr_variants__freq",
            "dr_variants__nucleotide_change",
            "dr_variants__locus_tag",
            "dr_variants__gene",
            "dr_variants___internal_change",
            "dr_resistances__drug",
            "dr_resistances__mutations",

            "other_variants__chr",
            "other_variants__genome_pos",
            "other_variants__type",
            "other_variants__change",
            "other_variants__freq",
            "other_variants__nucleotide_change",
            "other_variants__locus_tag",
            "other_variants__gene",
            "other_variants___internal_change",

            "sequence__project__id",
            "sequence__project__title",
            "owner__username",
            "sequence__LibrarySource",
            "sequence__LibraryLayout",
            "sequence__SequencerModel",
            "sequence__CenterName",
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

class ProfileSearchFilter(EbsSearchFilter):
    def __init__(self):
        self.nested_fields =  [
             "lineage__lin",
            "lineage__family",
            "lineage__spoligotype",
            "lineage__rd",
            "lineage__frac",
            "dr_variants__chr",
            "dr_variants__genome_pos",
            "dr_variants__type",
            "dr_variants__change",
            "dr_variants__freq",
            "dr_variants__nucleotide_change",
            "dr_variants__locus_tag",
            "dr_variants__gene",
            "dr_variants___internal_change",
            "dr_resistances__drug",
            "dr_resistances__mutations",

            "other_variants__chr",
            "other_variants__genome_pos",
            "other_variants__type",
            "other_variants__change",
            "other_variants__freq",
            "other_variants__nucleotide_change",
            "other_variants__locus_tag",
            "other_variants__gene",
            "other_variants___internal_change",
        ]
        self.nested_cats = [
            'lineage',
            'dr_variants',
            'other_variants',
            'dr_resistances'
           
        ]