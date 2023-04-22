from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status,generics
from .models import TPR
from .serializers import TPRSerializers
from student.models import Student
# Create your views here.

class TPRListView(generics.ListCreateAPIView):
    queryset=TPR.objects.all()
    serializer_class = TPRSerializers

class TPRView(generics.RetrieveDestroyAPIView):
    queryset = TPR.objects.all()
    serializer_class=TPRSerializers