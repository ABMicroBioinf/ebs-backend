from .models import Profile, Psummary
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
class LineageFilter(Filter):
    # only for depth = 2
    
    def filter(self, qs, value):
        if value in EMPTY_VALUES:
            return qs
        hierarchy = self.field_name.split("__")
        qs = qs.filter(lineage={hierarchy[1]: value})
        """ from django.db import connection
        print(connection.queries) """
        
        return 
        
class DrVariantFilter(Filter):
    # only for depth = 2
    
    def filter(self, qs, value):
        if value in EMPTY_VALUES:
            return qs
        hierarchy = self.field_name.split("__")
        qs = qs.filter(dr_variants ={hierarchy[1]: num(value)})
        """ from django.db import connection
        print(connection.queries) """
        return qs

class OtherVariantFilter(Filter):
    # only for depth = 2
    
    def filter(self, qs, value):
        if value in EMPTY_VALUES:
            return qs
        hierarchy = self.field_name.split("__")
        qs = qs.filter(other_variants ={hierarchy[1]: num(value)})
        """ from django.db import connection
        print(connection.queries) """
        return qs

class DrResistancesFilter(Filter):
    # only for depth = 2
    
    def filter(self, qs, value):
        if value in EMPTY_VALUES:
            return qs
        hierarchy = self.field_name.split("__")
        qs = qs.filter(dr_resistances ={hierarchy[1]: num(value)})
        """ from django.db import connection
        print(connection.queries) """
        return qs


class PsummaryFilter(filters.FilterSet): 
   
    id = CharFilter(lookup_expr="iexact")
    sequence__Projectid = CharFilter(lookup_expr="iexact")
    owner__username = CharFilter(lookup_expr="iexact")
    DateCreated = DateFromToRangeFilter()
    LastUpdate = DateFromToRangeFilter()
    Description = CharFilter(lookup_expr="icontains")

    pct_reads_mapped =  NumberFilter(lookup_expr="exact")
    num_reads_mapped = NumberFilter(lookup_expr="exact")
    main_lin = CharFilter(lookup_expr="iexact")
    sublin = CharFilter(lookup_expr="iexact")
    num_dr_variants = NumberFilter(lookup_expr="exact")
    num_other_variants = NumberFilter(lookup_expr="exact")
    drtype = CharFilter(lookup_expr="iexact")
    rifampicin = CharFilter(lookup_expr="iexact")
    isoniazid = CharFilter(lookup_expr="iexact")
    pyrazinamide = CharFilter(lookup_expr="iexact")
    ethambutol = CharFilter(lookup_expr="iexact")
    streptomycin = CharFilter(lookup_expr="iexact")
    fluoroquinolones = CharFilter(lookup_expr="iexact")
    moxifloxacin = CharFilter(lookup_expr="iexact")
    ofloxacin = CharFilter(lookup_expr="iexact")
    levofloxacin = CharFilter(lookup_expr="iexact")
    ciprofloxacin = CharFilter(lookup_expr="iexact")
    aminoglycosides = CharFilter(lookup_expr="iexact")
    amikacin = CharFilter(lookup_expr="iexact")
    kanamycin = CharFilter(lookup_expr="iexact")
    capreomycin = CharFilter(lookup_expr="iexact")
    ethionamide = CharFilter(lookup_expr="iexact")
    para_aminosalicylic_acid = CharFilter(lookup_expr="iexact")
    cycloserine = CharFilter(lookup_expr="iexact")
    linezolid = CharFilter(lookup_expr="iexact")
    bedaquiline = CharFilter(lookup_expr="iexact")
    clofazimine = CharFilter(lookup_expr="iexact")
    delamanid = CharFilter(lookup_expr="iexact")
    

class ProfileFilter(filters.FilterSet): 
    owner__username = CharFilter(lookup_expr="iexact")
    sequence__Projectid = CharFilter(lookup_expr="iexact")
    id = CharFilter(lookup_expr="iexact")
    sequence__Projectid = CharFilter(lookup_expr="iexact")
    owner__username = CharFilter(lookup_expr="iexact")
    DateCreated = DateFromToRangeFilter()
    LastUpdate = DateFromToRangeFilter()
    Description = CharFilter(lookup_expr="icontains")

    pct_reads_mapped =  NumberFilter(lookup_expr="exact")
    num_reads_mapped = NumberFilter(lookup_expr="exact")
    main_lin = CharFilter(lookup_expr="iexact")
    sublin = CharFilter(lookup_expr="iexact")
    num_dr_variants = NumberFilter(lookup_expr="exact")
    num_other_variants = NumberFilter(lookup_expr="exact")
    drtype = CharFilter(lookup_expr="iexact")
    
    
    lineage__lin = LineageFilter(
        field_name="lineage__lin", lookup_expr="iexact"
    )
    lineage__family = LineageFilter(
        field_name="lineage__family", lookup_expr="iexact"
    )
    lineage__spoligotype = LineageFilter(
        field_name="lineage__spoligotype", lookup_expr="iexact"
    )
    lineage__rd = LineageFilter(
        field_name="lineage__rd", lookup_expr="iexact"
    )
    lineage__frac = LineageFilter(
        field_name="lineage__frac", lookup_expr="iexact"
    )

    dr_variants__chr = DrVariantFilter(
        field_name="dr_variants__chr", lookup_expr="iexact"
    )
    dr_variants__genome_pos = DrVariantFilter(
        field_name="dr_variants__genome_pos", lookup_expr="iexact"
    )
    dr_variants__type = DrVariantFilter(
        field_name="dr_variants__type", lookup_expr="iexact"
    )
    dr_variants__change = DrVariantFilter(
        field_name="dr_variants__change", lookup_expr="iexact"
    )
    dr_variants__freq = DrVariantFilter(
        field_name="dr_variants__freq", lookup_expr="iexact"
    )
    dr_variants__nuceotide_change = DrVariantFilter(
        field_name="dr_variants__nuceotide_change", lookup_expr="iexact"
    )
    dr_variants__locus_tag = DrVariantFilter(
        field_name="dr_variants__locus_tag", lookup_expr="iexact"
    )
    dr_variants__gene = DrVariantFilter(
        field_name="dr_variants__gene", lookup_expr="iexact"
    )
    dr_variants___internal_change = DrVariantFilter(
        field_name="dr_variants___internal_change ", lookup_expr="iexact"
    )

    
    other_variants__chr = OtherVariantFilter(
        field_name="other_variants__chr", lookup_expr="iexact"
    )
    other_variants__genome_pos = OtherVariantFilter(
        field_name="other_variants__genome_pos", lookup_expr="iexact"
    )
    other_variants__type = OtherVariantFilter(
        field_name="other_variants__type", lookup_expr="iexact"
    )
    other_variants__change = OtherVariantFilter(
        field_name="other_variants__change", lookup_expr="iexact"
    )
    other_variants__freq = OtherVariantFilter(
        field_name="other_variants__freq", lookup_expr="iexact"
    )
    other_variants__nuceotide_change = OtherVariantFilter(
        field_name="other_variants__nuceotide_change", lookup_expr="iexact"
    )
    other_variants__locus_tag = OtherVariantFilter(
        field_name="other_variants__locus_tag", lookup_expr="iexact"
    )
    other_variants__gene = OtherVariantFilter(
        field_name="other_variants__gene", lookup_expr="iexact"
    )
    other_variants___internal_change = OtherVariantFilter(
        field_name="other_variants___internal_change", lookup_expr="iexact"
    )

    dr_resistances__drug = DrResistancesFilter(
        field_name="dr_resistance__drug", lookup_expr="iexact"
    )
    dr_resistances__mutations = DrResistancesFilter(
        field_name="dr_resistance__mutations", lookup_expr="iexact"
    )


