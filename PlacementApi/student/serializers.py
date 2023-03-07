from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from course.models import *
from django.db.models import Q


class PPOSerializer(serializers.ModelSerializer):
    company = serializers.SlugRelatedField(queryset = Company.objects.all(),slug_field='name')
    student = serializers.CharField(source = 'student.roll.username')

    class Meta:
        model = PPO
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class BranchSerializer(serializers.ModelSerializer):
    course = serializers.SlugRelatedField(queryset = Course.objects.all(),slug_field='name')
    class Meta:
        model = Specialization
        exclude = ['id']

class CitySerializer(serializers.ModelSerializer):
    state = serializers.SlugRelatedField(queryset = State.objects.all(),slug_field='name')
    class Meta:
        model = City
        exclude = ['id']



class ClusterChosenSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClusterChosen
        exclude = ['student','id']

class StudentSerializer(serializers.ModelSerializer):
    # roll = UserSerializer()
    roll = serializers.SlugRelatedField(queryset = User.objects.all(),slug_field='username')
    # roll  = serializers.CharField(source = 'roll.username')
    # course = CourseSerializer()
    course = serializers.SlugRelatedField(queryset = Course.objects.all(),slug_field='name')
    branch = BranchSerializer(read_only=True)
    branchWrite = serializers.CharField(write_only=True)
    city = CitySerializer(read_only=True)
    cityWrite = serializers.CharField(write_only=True)
    state = serializers.SlugRelatedField(queryset = State.objects.all(),slug_field='name', write_only=True)
    isBanned = serializers.SerializerMethodField(read_only=True)
    # student_placement = StudentPlacementSerializer(read_only = True,required = False)
    # student_intern = StudentInternSerializer(read_only = True,required = False)

    def get_isBanned(self,item):
        return (item.banned_date < timezone.now() and item.over_date > timezone.now())
    
    class Meta:
        model = Student
        fields = '__all__'

    def create(self, validated_data):
        course_data = validated_data["course"]
        branch_data = validated_data.pop('branchWrite')
        branch = Specialization.objects.get(Q(branch_name = branch_data) & Q(course = course_data))

        state_data = validated_data.pop('state')
        city_data = validated_data.pop('cityWrite')
        city = City.objects.get(Q(state__name = state_data) & Q(name = city_data))

        student = Student(branch=branch, city=city,**validated_data)
        student.save()
        return student

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name',instance.first_name)
        instance.middle_name = validated_data.get('middle_name',instance.middle_name)
        instance.last_name = validated_data.get('last_name',instance.last_name)
        instance.personal_email = validated_data.get('personal_email',instance.personal_email)
        instance.gender =  validated_data.get('gender',instance.gender)
        instance.pnumber = validated_data.get('pnumber',instance.pnumber)
        instance.dob = validated_data.get('dob',instance.dob)
        instance.current_year = validated_data.get('current_year',instance.current_year)
        instance.category = validated_data.get('category',instance.category)
        instance.cgpi = validated_data.get('cgpi',instance.cgpi)
        instance.gate_score = validated_data.get('gate_score',instance.gate_score)
        instance.cat_score = validated_data.get('cat_score',instance.cat_score)
        instance.class_10_year = validated_data.get('class_10_year',instance.class_10_year)
        instance.class_10_perc = validated_data.get('class_10_perc',instance.class_10_perc)
        instance.class_12_year = validated_data.get('class_12_year',instance.class_12_year)
        instance.class_12_perc = validated_data.get('class_12_perc',instance.class_12_perc)
        instance.active_backlog = validated_data.get('active_backlog',instance.active_backlog)
        instance.total_backlog = validated_data.get('total_backlog',instance.total_backlog)
        instance.linkedin = validated_data.get('linkedin',instance.linkedin)
        instance.save()
        return instance


class StudentPlacementSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only = True)
    cluster = ClusterChosenSerializer()
    roll = serializers.CharField(write_only = True)

    class Meta:
        model = StudentPlacement
        fields = '__all__'

    def create(self,validated_data):
        print(validated_data)
        cluster_1 = validated_data["cluster"].get('cluster_1')
        cluster_2 = validated_data["cluster"].get('cluster_2')
        cluster_3 = validated_data["cluster"].get('cluster_3')
        validated_data.pop('cluster')
        resume = validated_data.get("resume")
        undertaking = validated_data.get("undertaking")
        roll = validated_data.pop('roll')

        student = Student.objects.get(roll__username = roll)

        student_placement = StudentPlacement(student = student,resume = resume,undertaking = undertaking)

        student_placement.save()

        cluster_chosen = ClusterChosen(student = student_placement,cluster_1 =  cluster_1,cluster_2 = cluster_2,cluster_3 = cluster_3)

        cluster_chosen.save()

        return student_placement


class StudentInternSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only = True)
    roll = serializers.CharField(write_only = True)
    class Meta:
        model = StudentIntern
        fields = ['student','resume','roll']

    def create(self,validated_data):
        roll = validated_data.pop("roll")
        # owner = validated_data.pop("owner")
        student_id = Student.objects.get(roll__username = roll)
        intern_student = StudentIntern(student = student_id,**validated_data)
        intern_student.save()
        return intern_student

class StudentNotSittingSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only = True)
    roll = serializers.CharField(write_only = True)
    class Meta:
        model = StudentNotSitting
        fields = '__all__'

    def create(self,validated_data):
        # owner = validated_data.pop("owner")
        roll = validated_data.pop("roll")
        student_id = Student.objects.get(roll__username = roll)
        not_sitting_student = StudentNotSitting(student = student_id,**validated_data)
        not_sitting_student.save()
        return not_sitting_student


class PlacedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Placed
        fields = '__all__'


class InternedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interned
        fields = '__all__'
