from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Product
from .serializers import ProductSerializer, ProductWithReviewsSerializer
from .permissions import IsModeratorPermission

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsModeratorPermission]

    def perform_create(self, serializer):
        user = self.request.user
        # Проверяем метод is_adult у пользователя (у вас он должен быть в кастомном user)
        if not hasattr(user, 'is_adult') or not user.is_adult():
            raise PermissionDenied(detail="Вам должно быть 18 лет, чтобы создать продукт.")
        serializer.save()

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated, IsModeratorPermission]

class ProductWithReviewsListView(generics.ListAPIView):
    queryset = Product.objects.prefetch_related('reviews')
    serializer_class = ProductWithReviewsSerializer
    permission_classes = [IsAuthenticated]
