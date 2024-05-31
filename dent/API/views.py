from django.shortcuts import render
from rest_framework import permissions, viewsets
from rest_framework.views import APIView

from .serializers import ProductSerializer
from django.db.models import Count
from parsers.models import ProductModel
# Create your views here.
from django.http import Http404, HttpResponseNotFound
from rest_framework.response import Response

class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = ProductModel.objects.all()
    serializer_class = ProductSerializer

class ProductsToFind(APIView):

    def get(self, request, art):

        to_send = ProductModel.objects.filter(articul=art)
        items = [(item.name, item.date, item.price, item.site) for item in to_send]
        return Response(items)


def dups(request, sl):
    print('aaaaaaaaaaa')

    duplicates = ProductModel.objects.values('articul').annotate(articul_count=Count('articul')).filter(articul_count__gt=1)
    records = ProductModel.objects.filter(articul__in=[item['articul'] for item in duplicates])

    print(ProductModel.objects.filter(articul=sl))

    return HttpResponseNotFound('hello')