# models.py
from django.db import models
from django.contrib.auth.models import User
from courses.models import Course

class Default(models.Model):
    image = models.URLField(max_length=100,null=True,blank=True,default=None)
    bio = models.TextField(null=True,blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)          
    class Meta:
        abstract = True

class Student(Default):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student_profile")
    courses = models.ManyToManyField(Course,blank=True,related_name='students') 
    def __str__(self):
        return self.user.username

class Instructor(Default):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="instructor_profile")  # related_name should be used correctly here
    total_students = models.PositiveIntegerField(default=0)
    expertise = models.CharField(max_length=255, null=True, blank=True)
    years_of_experience = models.IntegerField(null=True, blank=True)
    qualifications = models.TextField(null=True, blank=True)
 
    def __str__(self):
        return self.user.username



# student = Student.objects.get(user=request.user)
# course = Course.objects.get(pk=course_id)
# student.purchased_courses.add(course)
