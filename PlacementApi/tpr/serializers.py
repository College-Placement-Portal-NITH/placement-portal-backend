from rest_framework import serializers
from .models import *

class TPRSerializers(serializers.ModelSerializer):
    name = serializers.SlugRelatedField(queryset=User.objects.all(),slug_field='username')
    course = serializers.SerializerMethodField()
    branch = serializers.SerializerMethodField()
    def get_course(self,object):
        try :
            name=object.name.student.course.name
        except:
            name=""
        return name
    def get_branch(self,object):
        try :
            name=object.name.student.branch.branch_fullname
        except:
            name=""
        return name
    class Meta:
        model = TPR
        fields = '__all__'

