from rest_framework import serializers
from .models import Role,JobRoles,Drive
from company.models import JNF_placement,JNF_intern,Company,JNF
from course.models import Specialization,Cluster
from course.serializers import SpecialisationSerializer
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class JobRolesSerializer(serializers.ModelSerializer):
    role = serializers.SlugRelatedField(queryset=Role.objects.all(), slug_field="name")
    # role = serializers.PrimaryKeyRelatedField(queryset = Role.objects.all())
    eligibleBatches = SpecialisationSerializer(many= True)
    # eligibleBatches = serializers.PrimaryKeyRelatedField(queryset = Specialization.objects.all(),many = True)
    drive = serializers.PrimaryKeyRelatedField(queryset = Drive.objects.all(),write_only = True)
    cluster = serializers.SlugRelatedField(queryset=Cluster.objects.all(),slug_field='cluster_id')
    # cluster_check = serializers.SerializerMethodField()
    class Meta:
        model = JobRoles
        fields = '__all__'

    # def get_cluster_check(self,obj):
    #     cluster = Cluster.objects.get(starting__lt = obj.ctc,ending__gte = obj.ctc)
    #     return (cluster==obj.cluster)




    def create(self, validated_data):
        print(validated_data)
        eligible_batches = validated_data.pop("eligibleBatches")
        job_role = JobRoles(**validated_data)
        job_role.save()
        for batches in eligible_batches:
            specialization = Specialization.objects.get(branchName = batches["branch"],course = batches["course"])
            job_role.eligible_batches.add(specialization)
        return job_role
    
    def update(self, instance, validated_data):
        print(validated_data)
        instance.drive = validated_data.get('drive',instance.drive)
        instance.role =  validated_data.get('role',instance.role)
        instance.ctc = validated_data.get('ctc',instance.ctc)
        instance.cgpi = validated_data.get('cgpi',instance.cgpi)
        branches = []
        for branch in validated_data["eligible_batches"]:
            print(branch)
            specialization = Specialization.objects.get(branchName = branch["branchName"],course = branch["course"])
            print(specialization)
            branches.append(specialization)
        # instance.eligible_batches.set(validated_data["eligible_batches"])
        instance.eligible_batches.set(branches)

        instance.save()
        return instance

    
from company.serializers import CompanySerializer
class DriveSerializer(serializers.ModelSerializer):
    company = serializers.SlugRelatedField(queryset =Company.objects.all(),slug_field="name")
    job_roles = JobRolesSerializer(read_only = True,many = True)
    image_url = serializers.ImageField(source = 'company.logo')
    
    class Meta:
        model = Drive
        fields = '__all__'

    def validate_job_desc_pdf(self, value):
        # print(value)
        return value
    
    def create(self,validated_data):
        # print(validated_data)
        jnf = None
        if validated_data["job_type"] == "intern" or validated_data["job_type"] == "intern and ppo":
            try:
                jnf = JNF_intern.objects.get(jnf__company = validated_data["company"])
            except:
                print("yes")
                # raise serializers.ValidationError("Corresponding intern details not found")
        elif validated_data["job_type"] == "placement":
            try:
                jnf = JNF_placement.objects.get(jnf__company = validated_data["company"])
            except:
                print("No")
                pass
                # raise serializers.ValidationError("Corresponding placement details not found")
        # validated_data["job_desc_pdf"] = jnf.job_desc_pdf

       
        drive = Drive(**validated_data)
        drive.save()
        return drive

    def update(self, instance, validated_data):
        name = validated_data["company"]

        instance.company = validated_data.get('company',instance.company)
        instance.ctc = validated_data.get('ctc_offered',instance.ctc)
        instance.modeOfHiring = validated_data.get('modeOfHiring',instance.modeOfHiring)
        instance.prePlacementTalk = validated_data.get('prePlacementTalk',instance.prePlacementTalk)
        instance.aptitudeTest = validated_data.get('aptitudeTest',instance.aptitudeTest)
        instance.technicalTest = validated_data.get('technicalTest',instance.technicalTest)
        instance.groupDiscussion = validated_data.get('groupDiscussion',instance.groupDiscussion)
        instance.personalInterview = validated_data.get('personalInterview',instance.personalInterview)
        instance.noOfPersonsVisiting = validated_data.get('noOfPersonsVisiting',instance.noOfPersonsVisiting)
        instance.jobLocation = validated_data.get('jobLocation',instance.jobLocation)
        instance.starting_date = validated_data.get('starting_date',instance.starting_date)
        instance.job_type = validated_data.get('job_type',instance.job_type)
        instance.ctc = validated_data.get('ctc',instance.ctc)
        instance.session = validated_data.get('session',instance.session)
        instance.save()
        return instance