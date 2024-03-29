from rest_framework import serializers
from student.models import Student 
from company.models import Company
from .models import Experience
from drive.models import Role

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['role']

class StudentListingField(serializers.RelatedField):
    def to_representation(self, value):
        return value.roll.username

    def to_internal_value(self, value):
        # print(Student.objects.get(roll__username = value))
        return Student.objects.get(roll__username = value)


class ExperienceSerializer(serializers.ModelSerializer):
    company = serializers.SlugRelatedField(queryset = Company.objects.all(),slug_field='name')
    company_image_url = serializers.SerializerMethodField()
    # student = serializers.SlugRelatedField(queryset = Student.objects.all(),slug_field='roll')
    # company = serializers.PrimaryKeyRelatedField(queryset = Company.objects.all()) 
    student = StudentListingField(queryset = Student.objects.all(),write_only = True)
    name = serializers.SerializerMethodField()
    roles = serializers.SlugRelatedField(queryset = Role.objects.all(),slug_field='name')
    # roles = serializers.PrimaryKeyRelatedField(queryset = Role.objects.all())
    description_read = serializers.SerializerMethodField()
    description = serializers.CharField(write_only = True)
    no_of_rounds = serializers.IntegerField(write_only = True)


    class Meta:
        model = Experience
        fields = '__all__'
    def get_company_image_url(self,obj):
        return  'https://tpoportal.pagekite.me/media/' + str(obj.company.logo)

    def get_name(self,obj):
        n = ""
        if obj.anonymity:
            n = ""
        else:
            n = obj.student.first_name
            if obj.student.last_name:
                n = n + " " +obj.student.last_name            
        return n
    def get_description_read(self,obj):
        return obj.description[:250]

    def create(self,validated_data):
        print(validated_data)
        experience = Experience(**validated_data)
        experience.save()
        return experience
    

class ExperienceDetailSerializer(serializers.ModelSerializer):
    company = serializers.SlugRelatedField(queryset = Company.objects.all(),slug_field='name')
    student = StudentListingField(queryset = Student.objects.all(),write_only = True)
    roles = serializers.SlugRelatedField(queryset = Role.objects.all(),slug_field='name')
    linkedin = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        model = Experience
        fields = '__all__'

    def get_name(self,obj):
        name = ""
        if obj.student.middle_name:
            name += obj.student.middle_name + " "
        return obj.student.first_name +" " + name + obj.student.last_name
        
    def get_linkedin(self,obj):
        return obj.student.linkedin    