from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django import views
from django.urls import reverse
from django.http import JsonResponse
from rest_framework import permissions, viewsets
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from .serializers import ProductSerializer, FileUploadSerializer
from django.db.models import Count
from django.core.files.storage import FileSystemStorage
from parsers.models import ProductModel, FileModel
# Create your views here.
from django.http import Http404, HttpResponseNotFound
from rest_framework.response import Response
from .handlers import xls_handler
import json

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

class SearchView(views.View):
    def get(self, request):
        slug = request.session.get('f.id')
        print(slug)
        out = []
        if slug:
            filename = f"out_data_{slug}.json"
            with open(filename, "r", encoding='utf8') as input_json:
                json_data = json.load(input_json)
                for key in json_data:
                    out.extend(json_data[key])
        return render(request, 'search.html', context={"data":out})


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = ProductModel.objects.all()
    serializer_class = ProductSerializer

class ProductsToFind(APIView):

    def get(self, request, art):
        if is_ajax(request=request):
            print("is_ajax")
        to_send = ProductModel.objects.filter(articul=art)
        items = [{"title":item.name,"date": item.date,"price": item.price,"site": item.site, "articul": item.articul} for item in to_send]
        return JsonResponse(items,safe=False, status=203)


class HandleXLS(APIView):
    queryset = FileModel.objects.all()
    def get(self, request):

        return render(request, 'fileupload.html')
    def post(self, request):
        # set 'data' so that you can use 'is_vaid()' and raise exception
        # if the file fails validation
        if request.FILES:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(f"data.{str(myfile.name).split('.')[1]}", myfile)
            uploaded_file_url = fs.url(filename)
            fn = xls_handler(uploaded_file_url)
        #print(request.FILES)
        
        request.session['f.id'] = fn
        print(request.session['f.id']) 
        return redirect('search')


def dups(request, sl):
    print('aaaaaaaaaaa')

    duplicates = ProductModel.objects.values('articul').annotate(articul_count=Count('articul')).filter(articul_count__gt=1)
    records = ProductModel.objects.filter(articul__in=[item['articul'] for item in duplicates])

    print(ProductModel.objects.filter(articul=sl))

    return HttpResponseNotFound('hello')