"""CRM_HACK URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls import url
from rest_framework import permissions
from common.views import index

openapi_info = openapi.Info(
    title='CRM_HACK API',
    default_version='v1'
)

schema = get_schema_view(
    openapi_info,
    public=True,
    permission_classes=(permissions.AllowAny,),
)



urlpatterns = [
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema.without_ui(cache_timeout=0), name='swagger-json'),
    url(r'^swagger/$', schema.with_ui("swagger", cache_timeout=0),  name="swagger-ui"),
    url(r'^redoc/$', schema.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path('api/', include('common.urls')),
    path('logout/', views.LogoutView, {'next_page': '/login/'}, name='logout'),
    path('', index),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
