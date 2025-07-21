from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Shop API",
      default_version='v1',
      description="API documentation",
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('', lambda request: redirect('/api/v1/')),
    path('admin/', admin.site.urls),
    path('api/v1/', include('product.urls')),
    path('api/v1/users/', include('users.urls')),

    # Swagger UI
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # Redoc UI
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
