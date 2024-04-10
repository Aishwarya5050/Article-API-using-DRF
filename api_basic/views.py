from django.db.models.query import QuerySet
from django.shortcuts import render

#Api import
from django.http import HttpResponse, JsonResponse
from rest_framework import serializers
from rest_framework import permissions
from rest_framework.parsers import JSONParser
from . models import Article
from . serializers import ArticleSerializers
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins
from rest_framework.authentication import SessionAuthentication, BaseAuthentication,TokenAuthentication 
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from django.shortcuts import get_object_or_404


# Viewsets
# Generic Viewsets

class ArticleViewset(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin,mixins.DestroyModelMixin):
    serializer_class = ArticleSerializers
    queryset = Article.objects.all()


#Model Viewsets
# the modelViewset is inherite from GenericAPI view. where all the data like get, post, put and delete is there.
class ArticleViewset(viewsets.ModelViewSet):
    serializer_class = ArticleSerializers
    queryset = Article.objects.all()


# in normal viewset, we need to add all methods by using traditional methods.
class ArticleViewset(viewsets.ViewSet ):
    def list(self, request):
        article = Article.objects.all()
        serializer = ArticleSerializers(article, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ArticleSerializers(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = Article.objects.all()
        article = get_object_or_404(queryset, pk=pk)
        serializer = ArticleSerializers(article)
        return Response(serializer.data)

    def update(self, request, pk=None):
        article= Article.objects.get(pk=pk)
        serializer = ArticleSerializers(article, data=request.data)
    
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
            
        return JsonResponse(serializer.errors, status=status.HTTP_404_NOT_FOUND)
 
#-----------------------------------------------------------------------------------------------------------------------

# Generic ApI views
# by using Generic view  we implemneted the following data

class GenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin):
    serializer_class = ArticleSerializers
    queryset = Article.objects.all()

    lookup_field ="id"
    # authentication_classes = [SessionAuthentication, BaseAuthentication]
    authentication_classes=[TokenAuthentication]
    permissions_classes = [IsAuthenticated]

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)
    
    def put(self, request, id=None):
        return self.update(request, id)

    def delete(self, request, id):
        return self.destroy(request, id)

#-----------------------------------------------------------------------------------------------------------------------

# API view
# by using API View class, where we can use get, post,put, delete method and import response ,status. 

class articleAPIView(APIView):
    def get(self, request):
        article = Article.objects.all()
        serializer = ArticleSerializers(article, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ArticleSerializers(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class articleDetailsView(APIView):
    def get_objects(self, id):
        try:
            return Article.objects.get(id=id)
        except Article.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        article = self.get_objects(id)
        serializer = ArticleSerializers(article)
        return Response(serializer.data)

    def put(self, request, id): 
        article= self.get_objects(id)
        serializer = ArticleSerializers(article, data=request.data)
    
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
            
        return JsonResponse(serializer.errors, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        article = self.get_objects(id)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#----------------------------------------------------------------------------------------------------------------------

# function based API view
# by using function based view where get and post method we apply. when we want to transfer that data that time we have to import api_view and  use like this @api_view

@api_view(['GET', 'POST'])
def article_list(request):
    if request.method == "GET":
        article = Article.objects.all()
        serializer = ArticleSerializers(article, many=True)
        return Response(serializer.data)
        # return JsonResponse(serializer.data, safe = False)

    elif request.method == 'POST':
        # data = JSONParser().parse(request)
        serializer = ArticleSerializers(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # return JsonResponse(serializer.errors, status=400)

@api_view(['GET', "PUT", "DELETE"])
def article_details(request, pk):
    try:
        article = Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
        # return HttpResponse(status=400)

    if request.method == "GET":
        serializer = ArticleSerializers(article)
        return Response(serializer.data)
        # return JsonResponse(serializer.data)

    elif request.method == "PUT":
        # data = JSONParser().parse(request)
        serializer = ArticleSerializers(article, data=request.data)
    
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
            # return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=status.HTTP_404_NOT_FOUND)
        # return JsonResponse(serializer.errors, status=404)

    elif request.method == "DELETE":
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        # return HttpResponse(status=204)

#  when we use a normal funtion that time we dont have to mention the things whic we reprentes in api_view based function.
#  in this class we use the JSONmodel and JSONResoponse and HTTPResponse and status like 404,201