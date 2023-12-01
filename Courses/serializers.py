from rest_framework import serializers
from .models import Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id_course', 'name', 'trainer', 'image_course',
                  'schedule_course', 'description_course', 'tuition_course']
