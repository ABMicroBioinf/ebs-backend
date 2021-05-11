from django.shortcuts import render
from account.models import Account
from study.models import Study
#from Study.views import get_project_queryset
from operator import attrgetter
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

# Create your views here.
PROJECTS_PER_PAGE = 1

# Create your views here.
def home_screen_view(request):
    #print(request.headers)
    context = {}
    # context['some_string'] = "this is some sting that I am going to pass"
    
    # accounts = Account.objects.all()
    # context['accounts'] = accounts

    studies = Study.objects.all()
    context['studies'] = studies
    return render(request, "home/home.html", context)

