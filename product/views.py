from rest_framework import generics
from django.db.models import Count
from .models import Category, Product, Review
from .serializers import (
    CategorySerializer, ProductSerializer, ReviewSerializer,
    ProductWithReviewsSerializer, CategoryWithCountSerializer
)

# --- CATEGORY VIEWS ---
class CategoryListView(generics.ListCreateAPIView):  # ← Добавили создание
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):  # ← Обновление + удаление
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'id'


# --- PRODUCT VIEWS ---
class ProductListView(generics.ListCreateAPIView):  # ← Добавили создание
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):  # ← Обновление + удаление
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'


# --- REVIEW VIEWS ---
class ReviewListView(generics.ListCreateAPIView):  # ← Добавили создание
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):  # ← Обновление + удаление
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    lookup_field = 'id'


# --- CUSTOM VIEWS (оставляем как есть) ---
class ProductWithReviewsListView(generics.ListAPIView):
    queryset = Product.objects.prefetch_related('reviews')
    serializer_class = ProductWithReviewsSerializer

class CategoryWithProductCountListView(generics.ListAPIView):
    queryset = Category.objects.annotate(products_count=Count('products'))
    serializer_class = CategoryWithCountSerializer
