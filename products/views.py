from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer, ProductDetailSerializer


@api_view(['GET'])
def product_detail_api_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(data={'error': 'Product not found!'},
                        status=status.HTTP_404_NOT_FOUND)
    data = ProductDetailSerializer(product).data
    return Response(data=data)


@api_view(http_method_names=['GET'])
def product_list_api_view(request):
    # step 1: Collect all products from DB (QuerySet)
    products = Product.objects.all()

    # step 2: Reformat (Serialize) data to list of Dictionary
    serializer = ProductSerializer(instance=products, many=True)

    # step 3: Return response with data and status (default: 200)
    return Response(data=serializer.data, status=status.HTTP_200_OK)
