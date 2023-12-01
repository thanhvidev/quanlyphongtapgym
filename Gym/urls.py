from django import views
from django.conf import settings
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from .views import ScheduleViewSet, ReviewViewSet, ChatMessageViewSet, NotificationViewSet, PaymentViewSet

router = DefaultRouter()
# router.register(r'schedules', ScheduleViewSet, basename='schedule')
# router.register(r'reviews', ReviewViewSet, basename='review')
# router.register(r'chat_messages', ChatMessageViewSet, basename='chat_message')
# router.register(r'notifications', NotificationViewSet, basename='notification')
# router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = [
    path('', views.home, name="home"),
    path('', include(router.urls)),
    path('notification', views.notification, name='notification'),
    path('search', views.search, name='search'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
