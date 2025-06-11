from django.db.models import Count
from rest_framework import generics
from .models import Category, Product, Review
from .serializers import (
    CategorySerializer, ProductSerializer, ReviewSerializer,
    ProductWithReviewsSerializer, CategoryWithCountSerializer
)

# Category views
class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'id'  # чтобы использовать <int:id> в urls.py

# Product views
class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'

# Review views
class ReviewListView(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class ReviewDetailView(generics.RetrieveAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    lookup_field = 'id'

class ProductWithReviewsListView(generics.ListAPIView):
    queryset = Product.objects.prefetch_related('reviews')
    serializer_class = ProductWithReviewsSerializer

class CategoryWithProductCountListView(generics.ListAPIView):
    queryset = Category.objects.annotate(products_count=Count('products'))
    serializer_class = CategoryWithCountSerializer
