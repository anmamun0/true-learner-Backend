from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseView ,VideoView

router = DefaultRouter()
router.register('courses',CourseView,basename='all_courses')
router.register('videos',VideoView,basename='all_videos')

urlpatterns = [
    path('',include(router.urls))
]