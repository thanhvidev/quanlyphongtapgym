from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet
from Courses import views

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')

urlpatterns = [
    # path('course/', views.courses, name='course'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('courses_by_schedule/', views.courses_by_schedule,
         name='courses_by_schedule'),
    path('category/<slug:category_slug>/',
         views.course_list, name='course_list'),
    path('category/<slug:category_slug>/<slug:course_slug>/',
         views.course_detail, name='course_detail'),
    path('', include(router.urls)),
]
