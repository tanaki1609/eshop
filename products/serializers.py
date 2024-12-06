from rest_framework import serializers
from .models import Product, Category, Tag


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = 'id name'.split()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = 'id name'.split()


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    tags = TagSerializer(many=True)
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = 'id reviews category category_name tags tag_names title text price'.split()
        depth = 1

    def get_category_name(self, product):
        if product.category_id:
            return product.category.name
        return ''


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
