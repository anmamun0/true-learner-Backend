from django.db import models
from django.contrib.auth.models import User , Group

class Course(models.Model):
    code = models.AutoField(primary_key=True) 
    instructor = models.ForeignKey(User,on_delete=models.CASCADE) 
    thumble = models.URLField(null=True,blank=True)
    title  = models.CharField(max_length=50)
    description = models.TextField()
    price = models.IntegerField()
    created_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def progress(self):
        total = self.videos.count()
        if total == 0:
            return 0
        completed = self.videos.filter(view=True).count()
        return int((completed  / total) * 100)
    

class Video(models.Model):
    order = models.AutoField(primary_key=True)  
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name='videos')
    title = models.CharField(max_length=100)
    url = models.URLField(max_length=150) 
    view = models.BooleanField(default=False)
    class Meta:
        ordering = ['order']
    def __str__(self):
        return self.title
    
