from rest_framework.routers import DefaultRouter
from .views import CustomUserViewSet
from django import views
from django.urls import include, path
from django.contrib.auth import views as auth_views
from . import views
from .views import TrainerProfileViewSet

router = DefaultRouter()
router.register(r'trainer_profiles', TrainerProfileViewSet,
                basename='trainer_profile')
router.register(r'users', CustomUserViewSet, basename='user')
urlpatterns = router.urls


urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.register_view, name='register'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('login/', views.login_view, name='login'),
    path('activateEmail/<user>/<to_email>/',
         views.activateEmail, name='activateEmail'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('change_avatar/', views.change_avatar, name='change_avatar'),
    path('course_purchased/', views.course_purchased, name='course_purchased'),
    path('schedule/', views.schedule, name='schedule'),
]
