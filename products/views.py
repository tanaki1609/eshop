from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer, ProductDetailSerializer


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail_api_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(data={'error': 'Product not found!'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = ProductDetailSerializer(product).data
        return Response(data=data)
    elif request.method == 'PUT':
        product.title = request.data.get('title')
        product.text = request.data.get('text')
        product.price = request.data.get('price')
        product.is_active = request.data.get('is_active')
        product.category_id = request.data.get('category_id')
        product.tags.set(request.data.get('tags'))
        product.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=ProductDetailSerializer(product).data)
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(http_method_names=['GET', 'POST'])
def product_list_api_view(request):
    if request.method == 'GET':
        # step 1: Collect all products from DB (QuerySet)
        products = (Product.objects.select_related('category')
                    .prefetch_related('tags', 'reviews').all())

        # step 2: Reformat (Serialize) data to list of Dictionary
        serializer = ProductSerializer(instance=products, many=True)

        # step 3: Return response with data and status (default: 200)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        # step 1: Receive data from RequestBody
        title = request.data.get('title')
        text = request.data.get('text', 'no text')
        price = request.data.get('price')
        is_active = request.data.get('is_active')
        category_id = request.data.get('category_id')
        tags = request.data.get('tags', [])

        # step 2: Create product by received data
        product = Product.objects.create(
            title=title,
            text=text,
            price=price,
            is_active=is_active,
            category_id=category_id,
        )
        product.tags.set(tags)
        product.save()

        # step 3: Return response as data and status
        return Response(status=status.HTTP_201_CREATED,
                        data=ProductDetailSerializer(product).data)
