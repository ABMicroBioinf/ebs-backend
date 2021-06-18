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


from django.conf.urls.static import static
from django.conf import settings

# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )

urlpatterns = [
    # Django Default Settings
    path('admin/', admin.site.urls),

    # API Settings
    path('api/account/', include('account.urls', 'account_api')),
    path('api/sandbox/', include('sandbox.urls', 'sandbox_api')),
    path('api/seq/', include('seq.urls', 'seq_api')),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('docs/', include_docs_urls(title='ebsAPI')),
    path('schema', get_schema_view(
        title="ebsAPI",
        description="API for the ebsAPI",
        version="1.0.0"
    ), name='openapi-schema'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)