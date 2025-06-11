from rest_framework import serializers
from .models import Category, Product, Review

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'



class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ProductWithReviewsSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'title', 'description', 'price', 'category', 'reviews', 'rating')

    def get_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews.exists():
            return round(sum([r.stars for r in reviews]) / reviews.count(), 2)
        return 0.0  # вместо None


class CategoryWithCountSerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'products_count')




