from djongo import models
from django_filters import rest_framework
from django_filters.filters import (
    CharFilter,
    DateFromToRangeFilter,
    Filter,
    NumberFilter,
) 
from .models import Assembly, Mlst, Resistome, Virulome, Annotation
from gizmos.filter import EbsSearchFilter, NestedFilter

#TODO: nested fields are not working with partial matching

class AssemblyFilter(rest_framework.FilterSet):
    
    class Meta:
        model = Assembly
        
        #equality-based filtering
        fields = [field.name for field in Assembly._meta.fields]
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

class MlstFilter(rest_framework.FilterSet):
    
    profile__locus = NestedFilter(
        field_name="profile__locus", lookup_expr="icontains"
    )
    profile__allele = NestedFilter(
        field_name="profile__allele", lookup_expr="iexact"
    )
    
    class Meta:
        model = Mlst
        
        #equality-based filtering
        fields = [field.name for field in Mlst._meta.fields]
        print(fields)
        fields.remove("owner")
        fields.remove("assembly")
        fields.remove("profile")
    
        extra = [
            "profile__allele",
            "profile__locus",
            "owner__username",
            "assembly__sequence__project__id",
            "assembly__sequence__project__title",
            "assembly__sequence__LibrarySource",
            "assembly__sequence__LibraryLayout",
            "assembly__sequence__SequencerModel",
            "assembly__sequence__CenterName",
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
    
    profile__geneName = NestedFilter(
        field_name="profile__geneName", lookup_expr="icontains"
    )
    profile__pctCoverage = NestedFilter(
        field_name="profile__pctCoverage", lookup_expr="icontains"
    )

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
            "profile__pctCoverage",
            "owner__username",
            "assembly__sequence__project__id",
            "assembly__sequence__project__title",
            "assembly__sequence__LibrarySource",
            "assembly__sequence__LibraryLayout",
            "assembly__sequence__SequencerModel",
            "assembly__sequence__CenterName",
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

class ResistomeSearchFilter(EbsSearchFilter):
    def __init__(self):
        self.nested_fields =  [
            "profile__geneName",
            "profile__pctCoverage",
        ]
        self.nested_cats = [
            'profile',
           
        ]

class VirulomeFilter(rest_framework.FilterSet):
    profile__geneName = NestedFilter(
        field_name="profile__geneName", lookup_expr="icontains"
    )
    profile__pctCoverage = NestedFilter(
        field_name="profile__pctCoverage", lookup_expr="icontains"
    )
    class Meta:
        model = Virulome
        fields = [field.name for field in Resistome._meta.fields]
        print(fields)
        fields.remove("owner")
        fields.remove("assembly")
        fields.remove("profile")
    
        extra = [
            "profile__geneName",
            "profile__pctCoverage",
            "owner__username",
            "assembly__sequence__project__id",
            "assembly__sequence__project__title",
            "assembly__sequence__LibrarySource",
            "assembly__sequence__LibraryLayout",
            "assembly__sequence__SequencerModel",
            "assembly__sequence__CenterName",
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

class AnnotationFilter(rest_framework.FilterSet):
   
    attr__tag = NestedFilter(
        field_name="attr__tag", lookup_expr="icontains"
    )
    attr__value = NestedFilter(
        field_name="attr__value", lookup_expr="icontains"
    )
    class Meta:
        model = Annotation
        fields = [field.name for field in Annotation._meta.fields]
        print(fields)
        fields.remove("owner")
        fields.remove("assembly")
        fields.remove("attr")
    
        extra = [
            "attr__tag",
            "attr__value",
            "owner__username",
            "assembly__sequence__project__id",
            "assembly__sequence__project__title",
            "assembly__sequence__LibrarySource",
            "assembly__sequence__LibraryLayout",
            "assembly__sequence__SequencerModel",
            "assembly__sequence__CenterName",
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


class AnnotationSearchFilter(EbsSearchFilter):
    def __init__(self):
        self.nested_fields =  [
            "attr__tag",
            "attr__value",
        ]
        self.nested_cats = [
            'attr',  
        ]