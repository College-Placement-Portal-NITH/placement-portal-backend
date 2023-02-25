from django.db import models
from student.models import Student
from django.utils import timezone
from django.core.validators import RegexValidator

# Create your models here.
class TPO(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()


class TPR(models.Model):
    name = models.ForeignKey(Student, on_delete=models.CASCADE)


class Announcement(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=500)
    type = models.CharField(max_length=100)
    description = models.TextField()
    session = models.CharField(max_length=7,validators=[RegexValidator(regex=r'\d{4}[-]\d{2}$')])
    time = models.DateTimeField(auto_now=True)
    tpo = models.ForeignKey(TPO, on_delete=models.CASCADE, null=True)
    tpr = models.ForeignKey(TPR, on_delete=models.CASCADE, null=True)

branch_choices = [
    ('cse','Computer Science and Engineering'),
    ('civil','Civil Engineering'),
    ('mech','Mechanical Engineering'),
    ('electrical','Electrical Engineering'),
    ('chemical','Chemical Engineering'),
    ('ece','Electronics and Communication Engineering'),
    ('material','Material Science and Engineering'),
    ('mnc','Mathematics and Computing'),
    ('eph','Engineering Physics'),
    ('archi','Architecture Engineering'),
    ('master','MBA'),
    ('sciences','Master in Sciences')
]

class Resources(models.Model):
    type = models.CharField(max_length=20, choices=[('management','Management'),('sciences','Sciences'),('tech','Technical')])
    branch = models.CharField(max_length=30,choices=branch_choices)
    heading = models.CharField(max_length=200)
    content_type = models.CharField(max_length=20, choices=[('article','Articles and Links'), ('faq','FAQs')])
    content = models.TextField()