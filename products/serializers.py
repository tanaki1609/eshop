from rest_framework import serializers
from .models import Product, Category, Tag
from rest_framework.exceptions import ValidationError


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


class ProductValidateSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, max_length=255, min_length=5)
    text = serializers.CharField(required=False)
    price = serializers.FloatField(max_value=1000000)
    is_active = serializers.BooleanField(default=False)
    category_id = serializers.IntegerField(min_value=1)
    tags = serializers.ListField(child=serializers.IntegerField(min_value=1))

    def validate_tags(self, tags):  # [1,2,1,100]
        tags = list(set(tags))  # [1,2]
        tags_from_db = Tag.objects.filter(id__in=tags)  # [1,2]
        if len(tags_from_db) != len(tags):
            raise ValidationError('Tag does not exist!')
        return tags

    def validate_category_id(self, category_id):
        try:
            Category.objects.get(id=category_id)
        except:
            raise ValidationError('Category does not exist!')
        return category_id


class ProductCreateSerializer(ProductValidateSerializer):
    def validate_title(self, title):
        if Product.objects.filter(title__exact=title):
            raise ValidationError('Product title already exists!')
        return title


class ProductUpdateSerializer(ProductValidateSerializer):
    def validate_title(self, title):
        product = self.context.get('product')
        if Product.objects.filter(title__exact=title).exclude(id=product.id):
            raise ValidationError('Product title already exists!')
        return title
