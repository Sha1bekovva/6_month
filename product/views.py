from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Product
from .serializers import ProductSerializer, ProductWithReviewsSerializer
from .permissions import IsModeratorPermission

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsModeratorPermission]

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated, IsModeratorPermission]

class ProductWithReviewsListView(generics.ListAPIView):
    queryset = Product.objects.prefetch_related('reviews')
    serializer_class = ProductWithReviewsSerializer
    permission_classes = [IsAuthenticated]
