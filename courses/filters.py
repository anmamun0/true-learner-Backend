from django_filters import FilterSet
import django_filters
from .models import Course,Video

class CourseFilter(FilterSet):
    code = django_filters.NumberFilter(field_name='code',lookup_expr='exact')
    title = django_filters.CharFilter(field_name='title',lookup_expr='icontains')
    instructor = django_filters.CharFilter(field_name='instructor__username', lookup_expr='icontains')  # Filter by instructor's username

    class Meta:
        model = Course
        fields = "__all__"

