from django.contrib import admin

# Register your models here.
from .models import Student,Instructor

admin.site.register(Student)
admin.site.register(Instructor)