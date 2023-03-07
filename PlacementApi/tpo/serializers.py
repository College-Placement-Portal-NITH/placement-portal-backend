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

# class CombinedSerializer(serializers.Serializer):
#     general_data = GeneralAnnouncementSerializer(many=True)
#     company_data = CompanyAnnouncementSerializer(many=True)
#     sorted_data = serializers.SerializerMethodField()

#     def get_sorted_data(self, obj):
#         combined_data = obj['general_data'] + obj['company_data']
        # sorted_data = sorted(combined_data, key=lambda x: x['updated_at'])
#         return sorted_data

# class CombinedSerializer(serializers.Serializer):
#     general = serializers.SerializerMethodField()
#     company = serializers.SerializerMethodField()
#     combined_data = serializers.SerializerMethodField()

#     def get_general(self, obj):
#         general = GeneralAnnouncement.objects.all().order_by('updated_at')
#         return GeneralAnnouncementSerializer(general, many=True).data

#     def get_company(self, obj):
#         company = CompanyAnnouncement.objects.all().order_by('updated_at')
#         return CompanyAnnouncementSerializer(company, many=True).data

#     def get_combined_data(self,obj):
#         print(obj)
#         combined_data = self.general.data + self.company.data
#         sorted_data = sorted(combined_data, key=lambda x: x['updated_at'])
#         return sorted_data

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resources
        fields = "__all__"