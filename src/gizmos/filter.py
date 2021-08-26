from djongo.models import Q
from rest_framework.compat import distinct
from rest_framework.filters import SearchFilter
import operator
from functools import reduce
#https://zhuanlan.zhihu.com/p/59072252
class EbsSearchFilter(SearchFilter):

    def __init__(self,nested_fields, nested_cats):
        self.nested_fields = nested_fields
        self.nested_cats = nested_cats
        super.__init__(self)

    def filter_queryset(self, request, queryset, view):
        search_fields = self.get_search_fields(view, request)
        search_terms = self.get_search_terms(request)

        print("*********************************")
        print(type(search_fields))
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

