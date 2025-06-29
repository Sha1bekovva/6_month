from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer, ProductWithReviewsSerializer
from django.db.models import Count

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'

class ProductWithReviewsListView(generics.ListAPIView):
    queryset = Product.objects.prefetch_related('reviews')
    serializer_class = ProductWithReviewsSerializer
