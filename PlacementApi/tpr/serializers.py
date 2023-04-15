from rest_framework import serializers
from .models import *
# from course.serializers import CourseSerializer,SpecialisationSerializer
# from django.contrib.auth.models import User

class UserSerializer(serializers.Serializer):
    username = serializers.CharField()

class CourseSerializer(serializers.Serializer):
    class Meta:
        model=Course
        fields=['id','name']

class SpecialisationSerializer(serializers.Serializer):
    class Meta:
        model=Course
        fields=['id','branch_name']

class TPRSerializers(serializers.ModelSerializer):
    name = UserSerializer()
    course = CourseSerializer()
    branch = SpecialisationSerializer()
    class Meta:
        model = TPR
        fields = '__all__'

