from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from django.db.models import Q
from django.utils import timezone
from product.models import Product
from product.serializers import ProductSerializer


# Create your views here.
class ProductViewSets(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductSerializer

    def get_queryset(self):
        query = self.request.query_params.get('query')
        if query:
            products = Product.objects.filter(Q(name__icontains=query) | Q(name_jamo__icontains=query))
        else:
            products = Product.objects.all()

        return products.filter(deleted_at__isnull=True).select_related('category').order_by('-created_at')

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

    def perform_destroy(self, instance):
        instance.deleted_at = timezone.now()
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
