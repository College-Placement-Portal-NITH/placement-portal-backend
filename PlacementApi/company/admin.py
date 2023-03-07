from django import forms
from django.contrib import admin
from .models import Company,HR_details,JNF,JNF_intern,JNF_placement
# Register your models here.

# admin.site.register(Company)
admin.site.register(JNF)
admin.site.register(JNF_intern)
admin.site.register(JNF_placement)
admin.site.register(HR_details)

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'
        widgets = {
            'svg_file': forms.FileInput(attrs={'accept': 'image/svg+xml'}),
        }

class CompanyAdmin(admin.ModelAdmin):
    form = CompanyForm

admin.site.register(Company, CompanyAdmin)