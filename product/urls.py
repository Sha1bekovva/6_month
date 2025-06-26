from django.urls import path
from .views import (
    ProductListView,
    ProductDetailView,
    ProductWithReviewsListView,
)

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:id>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/reviews/', ProductWithReviewsListView.as_view(), name='product-reviews'),
]
