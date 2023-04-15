from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import TPR
from .serializers import TPRSerializers
# Create your views here.

class TPRListView(APIView):
    def get(self,request):
        tpr=TPR.objects.select_related('name').all()
        serializer = TPRSerializers(tpr,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request):
        serializer= TPRSerializers(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
class TPRView(APIView):
    def get(self,request,pk,format=None):
        tpr=TPR.objects.get(id=pk)
        serializer = TPRSerializers(tpr)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def delete(self,request,pk,format=None):
        tpr = TPR.objects.get(id = pk)
        print(tpr)
        tpr.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
