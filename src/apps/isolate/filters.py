from djongo import models
from django_filters import rest_framework
from django_filters.filters import (
    CharFilter,
    DateFromToRangeFilter,
    Filter,
    NumberFilter,
    RangeFilter,
  
) 
from rest_framework.filters import SearchFilter
import django_filters
from .models import (
    Assembly, 
    Stats, 
    Mlst, 
    Resistome, 
    Virulome,
    Plasmid,
    TbProfileSummary, 
    TbProfile
)
from gizmos.filter import (
    EbsSearchFilter, 
    NestedFilter, 
    MultipleCharValueFilter,
    NumberRangeFilter,
    MultipleNumberRangeFilter
)

    
#TODO: nested fields are not working with partial matching

class AssemblyFilter(rest_framework.FilterSet):
    seqtype = MultipleCharValueFilter(lookup_expr="in")
    #sequence__project__id = MultipleCharValueFilter(lookup_expr="in")
    biosample__project__id = MultipleCharValueFilter(lookup_expr="in")
    
    #http://localhost:8000/api/isolate/assembly/?count_range=100,200
    min_count = django_filters.NumberFilter(field_name="count", lookup_expr='gte')
    max_count = django_filters.NumberFilter(field_name="count", lookup_expr='lte')
    min_bp = django_filters.NumberFilter(field_name="bp", lookup_expr='gte')
    max_bp = django_filters.NumberFilter(field_name="bp", lookup_expr='lte')
  
    class Meta:
        model = Assembly
        #equality-based filtering
        fields = [field.name for field in Assembly._meta.fields]
        fields.remove("owner")
        #fields.remove("project")
        extra = [
            # "sequence__project__id",
            # "sequence__project__title",
            # "sequence__LibrarySource",
            # "sequence__LibraryLayout",
            # "sequence__SequencerModel",
            # "sequence__CenterName",
            # "owner__username",
            #"biosample__project__id ",
            "biosample__project__id",
            "min_count",
            "max_count",
            "min_bp",
            "max_bp"
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
    #from rest_framework import filters  

#only works on text, char field, this is the generic text search
class AssemblySearchFilter(SearchFilter):
    class Meta:
        model = Assembly
        #equality-based filtering
        fields = [field.name for field in Assembly._meta.fields]
        fields.remove("owner")
        #fields.remove("sequence")
        exclude = [ 'count', 'bp', 'Ns', 'gaps', 'min', 'max', 'avg', 'N50']
        extra = [
           """  "sequence__project__id",
            "sequence__project__title",
            "sequence__LibrarySource",
            "sequence__LibraryLayout",
            "sequence__SequencerModel",
            "sequence__CenterName", """
            
             "biosample__project__id",
           
            "owner__username",
        ]
        fields = fields + extra
        
        
class StatsFilter(rest_framework.FilterSet):
    assembly__biosample__project__id = MultipleCharValueFilter(lookup_expr="in")
    assembly__biosample__sampleType= MultipleCharValueFilter(lookup_expr="in")
   
    class Meta:
        model = Stats
        
        #equality-based filtering
        fields = [field.name for field in Stats._meta.fields]
        fields.remove("owner")
        fields.remove("assembly")
        """ 
        extra = [
            "owner__username",
            "assembly__biosample__project__id",
            "assembly__biosample__project__title",
            # "assembly__biosample__LibrarySource",
            # "assembly__biosample__LibraryLayout",
            # "assembly__biosample__SequencerModel",
            # "assembly__biosample__CenterName",
          
        ]
        fields = fields + extra """
        
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
#only works on text, char field, this is the generic text search
class StatsSearchFilter(SearchFilter):
    class Meta:
        model = Assembly
        
        fields = [
            'id',
           # 'seqtype'
        ]
        extra = [
             "owner__username",
            "assembly__biosample__project__id",
            "assembly__biosample__project__title",
            "assembly__biosample__sampleType",
        ]
        fields = fields + extra
        

class MlstFilter(rest_framework.FilterSet):
    assembly__biosample__project__id = MultipleCharValueFilter(lookup_expr="in")
    assembly__biosample__sampleType= MultipleCharValueFilter(lookup_expr="in")
   
    profile__locus = NestedFilter(
        field_name="profile__locus", lookup_expr="icontains"
    )
    profile__alleleId = NestedFilter(
        field_name="profile__alleleId", lookup_expr="iexact"
    )
    
    #seqtype = MultipleCharValueFilter(lookup_expr="in")
    scheme = MultipleCharValueFilter(lookup_expr="in")
    st = MultipleCharValueFilter(lookup_expr="in")
    
    class Meta:
        model = Mlst
        
        #equality-based filtering
        fields = [field.name for field in Mlst._meta.fields]
        #print(fields)
        fields.remove("owner")
        fields.remove("assembly")
        fields.remove("profile")
    
        """   extra = [
            "profile__alleleId",
            "profile__locus",
            "owner__username",
            "assembly__biosample__project__id",
            "assembly__biosample__project__title",
            # "assembly__biosample__LibrarySource",
            # "assembly__biosample__LibraryLayout",
            # "assembly__biosample__SequencerModel",
            # "assembly__biosample__CenterName",
        ]
        fields = fields + extra """
        
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

class MlstSearchFilter(EbsSearchFilter):
    def __init__(self):
        self.nested_fields =  [
            "profile__locus",
            "profile__allele",
        ]
        self.nested_cats = [
            'profile',
           
        ]


class ResistomeFilter(rest_framework.FilterSet):
    assembly__biosample__project__id = MultipleCharValueFilter(lookup_expr="in")
    assembly__biosample__sampleType= MultipleCharValueFilter(lookup_expr="in")
    profile__geneName = NestedFilter(
        field_name="profile__geneName", lookup_expr="icontains"
    )
    profile__sequenceName = NestedFilter(
        field_name="profile__sequenceName", lookup_expr="icontains"
    )
    profile__scope = NestedFilter(
        field_name="profile__scope", lookup_expr="icontains"
    )
    profile__elementType = NestedFilter(
        field_name="profile__elementType", lookup_expr="icontains"
    )
    profile__dclass = NestedFilter(
        field_name="profile__dclass", lookup_expr="icontains"
    )
    profile__method = NestedFilter(
        field_name="profile__method", lookup_expr="icontains"
    )
    
    profile__pctCoverage = NestedFilter(
        field_name="profile__pctCoverage", lookup_expr="iexact"
    )
    profile__pctIdentity = NestedFilter(
        field_name="profile__pctIdentity", lookup_expr="iexact"
    ) 
    seqtype = MultipleCharValueFilter(lookup_expr="in")
    num_found = MultipleCharValueFilter(lookup_expr="in")
    class Meta:
        model = Resistome 
        #equality-based filtering
        fields = [field.name for field in Resistome._meta.fields]
        print(fields)
        fields.remove("owner")
        fields.remove("assembly")
        fields.remove("profile")
        
        extra = [
            "profile__geneName",
            "profile__sequenceName",
            "profile__scope",
            "profile__elementType",
            "profile__dclass",
            "profile__method",
            "profile__pctCoverage",
            "profile__pctIdentity",
            "owner__username",
            "assembly__biosample__project__id",
            "assembly__biosample__project__title",
            "assembly__biosample__sampleType",
            # "assembly__biosample__LibrarySource",
            # "assembly__biosample__LibraryLayout",
            # "assembly__biosample__SequencerModel",
            # "assembly__biosample__CenterName",
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
            }
        }

class ResistomeSearchFilter(EbsSearchFilter):
    def __init__(self):
        self.nested_fields =  [
            "profile__geneName",
            "profile__sequenceName",
            "profile__scope",
            "profile__elementType",
            "profile__dclass",
            "profile__method",
            # "profile__pctCoverage",
            # "profile__pctIdentity",
        ]
        self.nested_cats = [
            'profile',
           
        ]
    class Meta:
        model = Resistome 
        #equality-based filtering
        fields = [field.name for field in Resistome._meta.fields]
        print(fields)
        fields.remove("owner")
        fields.remove("assembly")
        fields.remove("profile")
    
        extra = [
            "profile__geneName",
            "profile__sequenceName",
            "profile__scope",
            "profile__elementType",
            "profile__dclass",
            "profile__method",
            "owner__username",
            "assembly__biosample__project__id",
            "assembly__biosample__project__title",
            "assembly__biosample__sampleType",
            # "assembly__biosample__LibrarySource",
            # "assembly__biosample__LibraryLayout",
            # "assembly__biosample__SequencerModel",
            # "assembly__biosample__CenterName",
        ]
        fields = fields + extra

class VirulomeFilter(rest_framework.FilterSet):
    assembly__biosample__project__id = MultipleCharValueFilter(lookup_expr="in")
    assembly__biosample__sampleType= MultipleCharValueFilter(lookup_expr="in")
    profile__geneName = NestedFilter(
        field_name="profile__geneName", lookup_expr="icontains"
    )
    profile__pctCoverage = NestedFilter(
        field_name="profile__pctCoverage", lookup_expr="icontains"
    ) 
   
    num_found = MultipleCharValueFilter(lookup_expr="in")
    class Meta:
        model = Virulome
        fields = [field.name for field in Resistome._meta.fields]
        #print(fields)
        fields.remove("owner")
        fields.remove("assembly")
        fields.remove("profile")
    
        extra = [
            "profile__geneName",
            "profile__pctCoverage",
            "owner__username",
            "assembly__biosample__project__id",
            "assembly__biosample__project__title",
            "assembly__biosample__sampleType",
            # "assembly__biosample__LibrarySource",
            # "assembly__biosample__LibraryLayout",
            # "assembly__biosample__SequencerModel",
            # "assembly__biosample__CenterName",
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

class VirulomeSearchFilter(EbsSearchFilter):
    def __init__(self):
        self.nested_fields =  [
            "profile__geneName",
            "profile__pctCoverage",
        ]
        self.nested_cats = [
            'profile',  
        ]
    class Meta:
        model = Virulome
        fields = [field.name for field in Resistome._meta.fields]
        #print(fields)
        fields.remove("owner")
        fields.remove("assembly")
        fields.remove("profile")
    
        extra = [
            "profile__geneName",
            "owner__username",
            "assembly__biosample__project__id",
            "assembly__biosample__project__title",
            "assembly__biosample__sampleType",
            # "assembly__biosample__LibrarySource",
            # "assembly__biosample__LibraryLayout",
            # "assembly__biosample__SequencerModel",
            # "assembly__biosample__CenterName",
        ]
        fields = fields + extra



class TbProfileSummaryFilter(rest_framework.FilterSet): 
   sequence__project__id = MultipleCharValueFilter(lookup_expr="in")
   main_lin = MultipleCharValueFilter(lookup_expr="in")
   sublin = MultipleCharValueFilter(lookup_expr="in")
   num_dr_variants = MultipleCharValueFilter(lookup_expr="in")
   num_other_variants = MultipleCharValueFilter(lookup_expr="in")
   drtype = MultipleCharValueFilter(lookup_expr="in")
   
   class Meta:
        model = TbProfileSummary
        
        #equality-based filtering
        fields = [field.name for field in TbProfileSummary._meta.fields]
        fields.remove("owner")
        fields.remove("sequence")
    
        """ extra = [
            "sequence__project__id",
            "sequence__project__title",
            "owner__username",
            "sequence__LibrarySource",
            "sequence__LibraryLayout",
            "sequence__SequencerModel",
            "sequence__CenterName",
        ]
        fields = fields + extra """
        
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

class TbProfileFilter(rest_framework.FilterSet): 
    
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
    sub_lin = MultipleCharValueFilter(lookup_expr="in")
    class Meta:
        model = TbProfile
        
        #equality-based filtering
        fields = [field.name for field in TbProfile._meta.fields]
        #print(fields)
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

class TbProfileSearchFilter(EbsSearchFilter):
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
        
class PlasmidFilter(rest_framework.FilterSet):
    assembly__biosample__project__id = MultipleCharValueFilter(lookup_expr="in")
    assembly__biosample__sampleType= MultipleCharValueFilter(lookup_expr="in")
   
    profile__contig_id = NestedFilter(
        field_name="profile__contig_id", lookup_expr="icontains"
    )
    profile__size = NestedFilter(
        field_name="profile__size", lookup_expr="iexact"
    )
  
    profile__mash_nearest_neighbor  = NestedFilter(
        field_name="profile__mash_nearest_neighbor", lookup_expr="iexact"
    )
    profile__mash_neighbor_identification  = NestedFilter(
        field_name="profile__mash_neighbor_identification", lookup_expr="iexact"
    )
    
    class Meta:
        model = Plasmid
        
        #equality-based filtering
        fields = [field.name for field in Plasmid._meta.fields]
        #print(fields)
        fields.remove("owner")
        fields.remove("assembly")
        fields.remove("profile")
        extra = [
            "profile__contig_id",
            "profile__size",
            "profile__mash_nearest_neighbor",
            "profile__mash_neighbor_identification",
            "assembly__biosample__project__id",
            "assembly__biosample__sampleType",
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

class PlasmidSearchFilter(EbsSearchFilter):
    def __init__(self):
        self.nested_fields =  [
            "profile__contig_id",
            "profile__size",
            "profile__mash_nearest_neighbor",
            "profile__mash_neighbor_identification"
        ]
        self.nested_cats = [
            'profile',
           
        ]
