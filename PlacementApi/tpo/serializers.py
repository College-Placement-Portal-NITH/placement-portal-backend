from rest_framework import serializers
from .models import GeneralAnnouncement, CompanyAnnouncement, Resources
from drive.models import Drive

class GeneralAnnouncementSerializer(serializers.ModelSerializer):
    # company = serializers.SlugRelatedField(queryset = Company.objects.all(),slug_field='name')
    # student = serializers.CharField(source = 'student.roll.username')
    class Meta:
        model = GeneralAnnouncement
        fields = '__all__'

class CompanyAnnouncementSerializer(serializers.ModelSerializer):
    # company = serializers.SlugRelatedField(queryset = Company.objects.all(),slug_field='name')
    # student = serializers.CharField(source = 'student.roll.username')
    drive = serializers.PrimaryKeyRelatedField(queryset=Drive.objects.all(), write_only=True)
    company_name = serializers.CharField(source='drive.company.name', read_only=True)
    job_type = serializers.CharField(source='drive.job_type', read_only=True)
    session = serializers.CharField(source='drive.session', read_only=True)
    class Meta:
        model = CompanyAnnouncement
        fields = '__all__'

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resources
        fields = "__all__"