#from django.conf.urls import include, re_path
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CompanyViewSet

app_name = "sandbox"
router = DefaultRouter()
#router.register('company', CompanyViewSet, basename='company')
router.register(r'company', CompanyViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 