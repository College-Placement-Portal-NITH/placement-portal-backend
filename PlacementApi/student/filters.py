import django_filters
from .models import Student,StudentPlacement,StudentNotSitting,StudentIntern,PPO, Placed, Offcampus
from course.models import Cluster
from django.db.models import Q, Exists, OuterRef, Subquery, F, Count, Max
from django.utils import timezone
from rest_framework import exceptions
import datetime

# class CharInFilter(django_filters.BaseInFilter, django_filters.CharFilter):
#     pass
class PPOFilter(django_filters.FilterSet):
    # company = CharInFilter(field_name='company__name',lookup_expr='in')
    company = django_filters.CharFilter(field_name='company__name',lookup_expr='iexact')
    student = django_filters.CharFilter(field_name='student__roll__username',lookup_expr='iexact')

    class Meta:
        model = PPO
        fields = ['session','company','student']

class StudentFilter(django_filters.FilterSet):
    student = django_filters.CharFilter(field_name='roll__username',lookup_expr='iexact')
    cgpi = django_filters.NumberFilter(field_name='cgpi',lookup_expr='gte')
    branch = django_filters.CharFilter(field_name='branch__branchName',lookup_expr='iexact')
    course =django_filters.CharFilter(field_name='course__name',lookup_expr='iexact')
    class Meta:
        model = Student
        fields = ['student','cgpi','branch','course','pwd']


class StudentTPOFilter(django_filters.FilterSet):
    chosenSession=""
    student = django_filters.CharFilter(field_name='roll__username',lookup_expr='iexact')
    cgpi = django_filters.NumberFilter(field_name='cgpi',lookup_expr='gte')
    branches = django_filters.CharFilter(field_name='branch__branchName',lookup_expr='iexact')
    course =django_filters.CharFilter(field_name='course__name',lookup_expr='iexact')
    eligibility = django_filters.CharFilter(method='filter_eligibility')
    session = django_filters.CharFilter(method='filter_session')

    minAge = django_filters.NumberFilter(method='filter_min_age')
    maxAge = django_filters.NumberFilter(method='filter_max_age')

    isBanned = django_filters.BooleanFilter(method='filter_isBanned')
    selected = django_filters.BooleanFilter(method='filter_isSelected')

    # filters for gap year
    gap12Ug = django_filters.NumberFilter(field_name='gap_12_ug')
    gapUgPg = django_filters.NumberFilter(field_name='gap_ug_pg')

    # placement related filters
    isNotSitting = django_filters.BooleanFilter(method='filter_isNotSitting')
    # filter for not sitting reason
    from .models import reasons
    notSittingReason = django_filters.ChoiceFilter(field_name='student_ns__reason', choices=reasons)

    placementType=django_filters.CharFilter(method='filter_placementType')
    isPlacedFirstCluster = django_filters.BooleanFilter(method='filter_isPlacedFirstCluster')

    isBasePlaced = django_filters.BooleanFilter(method='filter_isBasePlaced')
    # isMiddlePlaced = django_filters.BooleanFilter(method='filter_isMiddlePlaced')
    # isDreamPlaced denotes placement in a cluster greater than or equal to third cluster
    isDreamPlaced = django_filters.BooleanFilter(method='filter_isDreamPlaced')

    class Meta:
        model = Student
        fields = ['student', 'cgpi', 'branch', 'course','pwd','gender', 'category','disability_type','disability_percentage','gap_12_ug','gap_ug_pg']

    def filter_eligibility(self, queryset, name, value):
        if value=="placement" or value=="both":
            return queryset.filter(student_placement__isnull=False)
        elif value=="internship":
            return queryset.filter(Q(student_intern__isnull=False) & Q(student_placement__isnull=True))
        elif value=="other":
            return queryset.filter(Q(student_placement__isnull=True) & Q(student_intern__isnull=True))
        else:
            print("Eligibility cannot be ", value)
            return queryset.filter()

    def filter_session(self, queryset, name, value):
        self.chosenSession = value

        from django.utils.regex_helper import _lazy_re_compile

        regex=r'\d{4}[-]\d{2}$'
        regex = _lazy_re_compile(regex, False)
        regex_matches = regex.search(str(value))
        invalid_input = not regex_matches
        if invalid_input:
            raise exceptions.NotAcceptable("Session does not match the regex")

        st_year = int(value[:4])
        en_year = int(value[:2] + value[5:])

        if en_year!=st_year+1:
            raise exceptions.NotAcceptable("Session must have only one year difference for e.g. 2022-23")

        return queryset.filter(batch_year__lte=st_year, passing_year__gt=st_year)

    def filter_min_age(self, queryset, name, value):
        if(value < 0):
            raise exceptions.NotAcceptable("Minimum age cannot be negative")
        today = datetime.date.today()
        min_date = today.replace(year=int(today.year-value))
        return queryset.filter(dob__lte=min_date)

    def filter_max_age(self, queryset, name, value):
        if(value<0):
            raise exceptions.NotAcceptable("Maximum age cannot be negative")
        today = datetime.date.today()
        max_date = today.replace(year=int(today.year-value-1))
        return queryset.filter(dob__gt=max_date)

    def filter_isBanned(self, queryset, name, value):
        if value:
            return queryset.filter(banned_date__lte=timezone.now(), over_date__gte=timezone.now())
        else:
            return queryset.exclude(banned_date__lte=timezone.now(), over_date__gte=timezone.now())

    def filter_isSelected(self, queryset, name, value):
        if value:
            return queryset.filter(Q(student_intern__student_interned__isnull=False) | Q(student_placement__student_placed__isnull=False) | Q(student_ppo__isnull=False) | Q(student_offcampus__isnull=False))
        else:
            return queryset.filter(Q(student_intern__student_interned__isnull=True) & Q(student_placement__student_placed__isnull=True) & Q(student_ppo__isnull=True) & Q(student_offcampus__isnull=True))

    def filter_isNotSitting(self, queryset, name, value):
        print(name, value)
        value = not value
        return queryset.filter(student_ns__isnull=value)

    def filter_placementType(self, queryset, name, value):
        if value=="offcampus":
            return queryset.filter(student_offcampus__isnull=False)
        elif value=="oncampus":
            return queryset.filter(student_placement__student_placed__isnull=False)
        elif value=="ppo":
            return queryset.filter(student_ppo__isnull=False)
        else:
            raise exceptions.NotAcceptable("placement type cannot be anything other than offcampus, oncampus, ppo")

    def filter_isPlacedFirstCluster(self, queryset, name, value):
        print(self.chosenSession)
        if self.chosenSession=="":
            raise exceptions.APIException("You cannot see the placement statistics because there is no session given in query parameters")

        try:
            # getting the object of cluster 1
            cluster = Cluster.objects.get(session=self.chosenSession, starting=0)
        except Cluster.DoesNotExist:
            raise exceptions.APIException("Cluster 1 for current session does not exist")

        subquery_placed = Placed.objects.filter(job_role__ctc__range=(cluster.starting, cluster.ending))
        subquery_ppo = PPO.objects.filter(ctc__range=(cluster.starting, cluster.ending))
        subquery_offcampus = Offcampus.objects.filter(ctc__range=(cluster.starting, cluster.ending))

        if value:
            return queryset.filter(Q(Exists(subquery_placed)) | Q(Exists(subquery_ppo)) | Q(Exists(subquery_offcampus)))
        else:
            return queryset.exclude(Q(Exists(subquery_placed)) | Q(Exists(subquery_ppo)) | Q(Exists(subquery_offcampus)))
            # return queryset.filter(~Exists(Placed.objects.filter(job_role__ctc__range=(cluster.starting, cluster.ending))))
            # return queryset.filter(~Exists(Placed.objects.filter(student=OuterRef('student_placement'))))

    def filter_isBasePlaced(self, queryset, name, value):
        subquery_placed = Placed.objects.filter(student__student__pk=OuterRef('pk'), job_role__ctc__gt=F('student__cluster__cluster_1__starting'), job_role__ctc__lte=F('student__cluster__cluster_2__starting')).annotate(count = Count('id')).values('count')
        subquery_ppo = PPO.objects.filter(student__pk=OuterRef('pk'), ctc__gt=F('student__student_placement__cluster__cluster_1__starting'), ctc__lte=F('student__student_placement__cluster__cluster_2__starting')).annotate(count = Count('id')).values('count')
        subquery_offcampus = Offcampus.objects.filter(student__pk=OuterRef('pk'), ctc__gt=F('student__student_placement__cluster__cluster_1__starting'), ctc__lte=F('student__student_placement__cluster__cluster_2__starting')).annotate(count = Count('id')).values('count')
        # query = Placed.objects.filter(job_role__ctc__range=(4,9)).annotate(count = Count('id')).values('count')
        if value:
            return queryset.filter(Q(Exists(subquery_placed)) | Q(Exists(subquery_ppo)) | Q(Exists(subquery_offcampus)))
        else:
            return queryset.exclude(Q(Exists(subquery_placed)) | Q(Exists(subquery_ppo)) | Q(Exists(subquery_offcampus)))
            # return queryset.filter(Q(~Exists(subquery_placed)) & Q(~Exists(subquery_ppo)) & Q(~Exists(subquery_offcampus)))

    def filter_isDreamPlaced(self, queryset, name, value):
        subquery_placed = Placed.objects.values('student').annotate(ctc=Max('job_role__ctc')).filter(student__student__pk=OuterRef('pk'), ctc__gte=F('student__cluster__cluster_2__starting')).annotate(count = Count('id')).values('count')
        subquery_ppo = PPO.objects.values('student').annotate(ctc=Max('ctc')).filter(student__pk=OuterRef('pk'), ctc__gte=F('student__student_placement__cluster__cluster_2__starting')).annotate(count = Count('id')).values('count')
        subquery_offcampus = Offcampus.objects.values('student').annotate(ctc=Max('ctc')).filter(student__pk=OuterRef('pk'), ctc__gte=F('student__student_placement__cluster__cluster_2__starting')).annotate(count = Count('id')).values('count')
        # query = Placed.objects.filter(job_role__ctc__range=(4,9)).annotate(count = Count('id')).values('count')
        if value:
            return queryset.filter(Q(Exists(subquery_placed)) | Q(Exists(subquery_ppo)) | Q(Exists(subquery_offcampus)))
        else:
            return queryset.exclude(Q(Exists(subquery_placed)) | Q(Exists(subquery_ppo)) | Q(Exists(subquery_offcampus)))
            # return queryset.filter(~Exists(subquery))


class StudentPlacementFilter(django_filters.FilterSet):
    student = django_filters.CharFilter(field_name='student__roll__username',lookup_expr='iexact')
    cgpi = django_filters.NumberFilter(field_name='student__cgpi',lookup_expr='gte')
    branch = django_filters.CharFilter(field_name='student__branch__branchName',lookup_expr='iexact')
    course =django_filters.CharFilter(field_name='student__course__name',lookup_expr='iexact')
    cluster = django_filters.CharFilter(method='filter_by_cluster')
    pwd = django_filters.BooleanFilter(field_name='student__pwd')
    class Meta:
        model = StudentPlacement
        fields = ['student','cgpi','branch','course','cluster','pwd']
    def filter_by_cluster(self,queryset,name,value):
        return queryset.filter(Q(cluster__cluster_1 = value) | Q(cluster__cluster_3 = value) | Q(cluster__cluster_2 = value))


class StudentInternFilter(django_filters.FilterSet):
    student = django_filters.CharFilter(field_name='student__roll__username',lookup_expr='iexact')
    cgpi = django_filters.NumberFilter(field_name='student__cgpi',lookup_expr='gte')
    branch = django_filters.CharFilter(field_name='student__branch__branchName',lookup_expr='iexact')
    course =django_filters.CharFilter(field_name='student__course__name',lookup_expr='iexact')
    pwd = django_filters.BooleanFilter(field_name='student__pwd')
    
    class Meta:
        model = StudentIntern
        fields = ['student','cgpi','branch','course','pwd']

class StudentNSFilter(django_filters.FilterSet):
    student = django_filters.CharFilter(field_name='student__roll__username',lookup_expr='iexact')
    cgpi = django_filters.NumberFilter(field_name='student__cgpi',lookup_expr='gte')
    branch = django_filters.CharFilter(field_name='student__branch__branchName',lookup_expr='iexact')
    course =django_filters.CharFilter(field_name='student__course__name',lookup_expr='iexact')
    reason = django_filters.CharFilter(field_name='reason',lookup_expr='iexact')
    class Meta:
        model = StudentNotSitting
        fields = ['student','cgpi','branch','course','reason']