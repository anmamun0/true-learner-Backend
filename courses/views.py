from django.shortcuts import render
from rest_framework import viewsets ,status , response
from .serializers import CourseSerializers, VideoSerializes
# Create your views here.
from .models import Course,Video

from .filters import CourseFilter
from django_filters import rest_framework

from rest_framework.decorators import action
from django.contrib.auth.models import User

from django.core.exceptions import ObjectDoesNotExist

class CourseView(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializers  
    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_class = CourseFilter

    @action(detail=True,methods=['post'],url_path='create')
    def course_create(self,request,pk=None):
        try:
            user = User.objects.get(pk=pk)  
            if not user.groups.filter(name='Instructor').exists():
                return response.Response({'error':"You'r not an Instructor"},status=status.HTTP_404_NOT_FOUND)
            
            # Extract data from the request
            title = request.data.get('title')
            description = request.data.get('description')  # Make sure the key matches
            price = request.data.get('price')
            
            course = Course.objects.create(
                instructor= user,
                title=title,
                description=description,
                price=price,
            )
            serializer = CourseSerializers(course)
            return response.Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            return response.Response({'error':str(e)},status=status.HTTP_501_NOT_IMPLEMENTED)
        
    @action(detail=True,methods=['post'],url_path='update')
    def course_create(self,request,pk=None):
        try:
            course = Course.objects.get(pk=pk) 
            course.title = request.data.get('title',course.title)
            course.description = request.data.get('description',course.title)  # Make sure the key matches
            course.price = request.data.get('price',course.title)
            course.save()
            
            serializer = CourseSerializers(course)
            return response.Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            return response.Response({'error':str(e)},status=status.HTTP_501_NOT_IMPLEMENTED)
        
from .models import Course,Video
class VideoView(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializes

    @action(detail=True,methods=['post'],url_path='create')
    def video_create(self,request,pk=None):
        try:
            course = Course.objects.get(pk=pk)
            title = request.data.get('title')
            url = request.data.get('url') 
            video = Video.objects.create(
                course=course,
                title=title,
                url=url,
            )
            serializer = VideoSerializes(video)
            return response.Response(serializer.data,status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return response.Response({'error':"invalid information!"},status=status.HTTP_400_BAD_REQUEST)
    @action(detail=True,methods=['put'],url_path='update')
    def video_update(self,request,pk=None):
        try:
            video = Video.objects.get(pk=pk)
            video.title = request.data.get('title',video.title)
            video.url = request.data.get('url',video.url)
            video.save()
            info = VideoSerializes(video)
            return response.Response(info.data,status=status.HTTP_200_OK)
        except Exception as e:
            return response.Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=True,methods=['post'],url_path='delete')
    def video_delete(self,request,pk=None):
        try:
            video = Video.objects.get(pk=pk)
            video.delete()
            return response.Response({'message':"Successfully video deleted!"},status=status.HTTP_200_OK)
        except Exception as e:
            return response.Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)