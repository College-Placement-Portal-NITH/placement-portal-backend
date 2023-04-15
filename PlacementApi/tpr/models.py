from django.db import models
from django.contrib.auth.models import User
from course.models import Course,Specialization

# Create your models here.
class TPR(models.Model):
    name = models.OneToOneField(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course,on_delete=models.CASCADE,null=True)
    branch = models.ForeignKey(Specialization,on_delete=models.CASCADE,null=True)
    def __str__(self):
        return self.name