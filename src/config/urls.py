"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from django.conf.urls.static import static
from django.conf import settings

from apps.account.api import MyTokenObtainPairView
from rest_framework_simplejwt.views import (
    #TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    # Django Default Settings
    path('admin/', admin.site.urls),

    # API Settings
    path('api/account/', include('apps.account.urls', 'account_api')),
    path('api/account/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/account/token/refresh/', TokenRefreshView.as_view(), name='my_token_refresh'),
    path('api/seq/', include('apps.seq.urls', 'seq_api')),
    path('api/mseq/', include('apps.mseq.urls', 'mseq_api')),
    path('api/isolate/', include('apps.isolate.urls', 'isolate_api')),
    #path('api/isolate/gbase/', include('apps.isolate.gbase.urls', 'isolate_gbase_api')),
    #path('api/isolate/tb/', include('apps.isolate.tb.urls', 'isolate_tb_api')),
    #path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    #path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('docs/', include_docs_urls(title='ebsAPI', permission_classes = [AllowAny], public=True)),
    path('schema', get_schema_view(
        title="ebs-backend API",
        description="API for the ebsAPI",
        version="1.0.0",
        permission_classes = [AllowAny],
    ), name='openapi-schema'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)