from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('/api/v1/')),
    path('admin/', admin.site.urls),
    path('api/v1/', include('product.urls')),
    path('api/v1/users/', include('users.urls')),  # если есть приложение users
]
