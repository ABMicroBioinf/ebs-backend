from djongo.models import Q
from rest_framework.compat import distinct
from rest_framework.filters import SearchFilter
import operator
from functools import reduce
from django_filters.filters import Filter, BaseRangeFilter, NumberFilter
from django_filters.constants import EMPTY_VALUES

#TODO 
#nested fields work well with string but not with number
class NestedFilter(Filter):
    # only for depth = 2
    # def __init__(self,field_parent):
    #     self.field_parent = field_parent
    #     super.__init__(self)

    def filter(self, qs, value):
        if value in EMPTY_VALUES:
            return qs
        hierarchy = self.field_name.split("__")
        d = {}
        d[hierarchy[0]] = {hierarchy[1]: value}
        print("testing nested fields..................................")
        print(d)
        #qs = qs.filter(profile={hierarchy[1]: value})
        qs = qs.filter(**d)
        from django.db import connection
        print(connection.queries) 
        
        return qs

class MultipleCharValueFilter(Filter):
    
    def filter(self, qs, value):
        print(type(self))
        print(self.field_name)
        if value in EMPTY_VALUES:
            return qs
        print(value)
        value_list = value.split(",")
        print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        print(value)
        print(value_list)
        print(type(value_list))
        mylist = []
       
        for item in value_list:
          mylist.append(item.replace("‑", ","))
          
        print(qs)
        qs = super().filter(qs, mylist)
        return qs
    

class NumberRangeFilter(BaseRangeFilter, NumberFilter):
   pass

#https://zhuanlan.zhihu.com/p/59072252
class EbsSearchFilter(SearchFilter):

    def __init__(self,nested_fields, nested_cats):
        self.nested_fields = nested_fields
        self.nested_cats = nested_cats
        super.__init__(self)

    def filter_queryset(self, request, queryset, view):
        search_fields = self.get_search_fields(view, request)
        search_terms = self.get_search_terms(request)

        print("I am in EbsSearchFilter*********************************")
        print("search_fields type=")
        print(type(search_fields))
        print("search_fields=")
        print(search_fields)

        if not search_fields or not search_terms:
            return queryset

        nested_target = list(set(search_fields) & set(self.nested_fields))
        regular_target = list(set(search_fields) - set(self.nested_fields))
        """ for test in regular_target:
            print(type(self.construct_search(test)))
            print(self.construct_search(test)) """

        
        orm_lookups = [
            self.construct_search(str(search_field))
            for search_field in regular_target
        ]

        nested_lookups = [
            self.construct_search(str(search_field))
            for search_field in nested_target
        ]

        base = queryset

        regular_qlist = []
        for search_term in search_terms:
            print(search_term)
            queries = [
                Q(**{orm_lookup: search_term})
                for orm_lookup in orm_lookups
            ]
            regular_qlist.append(reduce(operator.or_, queries))
        regular_queryset = queryset.filter(reduce(operator.and_, regular_qlist))

        nested_conditions = []
        for search_term in search_terms:
           
            nested_qlist = []
            for nested_lookup in nested_lookups:
                for nested_cat in self.nested_cats:
                    tag = nested_lookup.split("__")[0]
                    value = nested_lookup.split("__")[1]
                    
                    d = {}
                    d[value] = search_term
                    if tag == nested_cat:
                        dd = {}
                        dd[nested_cat] = d
                        nested_qlist.append(Q(**dd))
                        print(nested_qlist)
                        
            
            print("nested_qlist.................................")
            print(nested_qlist)
            nested_conditions.append(reduce(operator.or_, nested_qlist))
            print(nested_conditions)
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

