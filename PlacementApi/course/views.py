from django.shortcuts import render
from rest_framework import generics
from .models import Course, Specialization
from .serializers import CourseSerializer, SpecializationSerializer
from rest_framework.response import Response

# Create your views here.
class CourseAPIView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class SpecializationAPIView(generics.ListCreateAPIView):
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer
    def post(self, request, *args, **kwargs):
        serializer = SpecializationSerializer(data=request.data)
        if serializer.is_valid():
            # serializer.save()
            return Response({"message":"Company data Inserted successfully"})
        else:
            print(serializer.errors)
            return Response(serializer.errors)
