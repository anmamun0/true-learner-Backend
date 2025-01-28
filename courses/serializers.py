from rest_framework import serializers
from .models import Course, Video

class VideoSerializes(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = "__all__"

class CourseSerializers(serializers.ModelSerializer):
    videos = VideoSerializes(read_only=True,many=True) 
    class Meta:
        model = Course
        fields = ['code','thumble','title','description','price','instructor','created_on','videos']


