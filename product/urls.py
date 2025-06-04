from django.urls import path
from django.http import JsonResponse
from .views import (
    CategoryListView, CategoryDetailView,
    ProductListView, ProductDetailView,
    ReviewListView, ReviewDetailView
)

def api_root(request):
    return JsonResponse({
        "categories": "/api/v1/categories/",
        "products": "/api/v1/products/",
        "reviews": "/api/v1/reviews/"
    })

urlpatterns = [
    path('', api_root),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:id>/', CategoryDetailView.as_view(), name='category-detail'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:id>/', ProductDetailView.as_view(), name='product-detail'),
    path('reviews/', ReviewListView.as_view(), name='review-list'),
    path('reviews/<int:id>/', ReviewDetailView.as_view(), name='review-detail'),
]
