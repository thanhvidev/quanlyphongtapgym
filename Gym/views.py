from django.db.models import Sum
from django.contrib import messages
from django.db import transaction
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView, DetailView
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from Gym.consumers import NotificationConsumer
from .models import *
from rest_framework import viewsets
from Courses.models import Category, Membership
# from .models import Schedule, Review, ChatMessage, Notification, Payment
# from .serializers import ScheduleSerializer, ReviewSerializer, ChatMessageSerializer, NotificationSerializer, PaymentSerializer


def home(request):
    category = None
    categories = Category.objects.all()
    courses = Course.objects.filter(is_active=True)
    context = {
        'category': category,
        'categories': categories,
        'courses': courses,
        'room_name': NotificationConsumer
    }
    return render(request, 'home.html', context)


def search(request):  # TÌM KIẾM
    if 'q' in request.GET:
        q = request.GET.get('q')
        courses = Course.objects.order_by(
            '-created_date').filter(Q(name__icontains=q))
        course_count = courses.count()
    context = {
        'courses': courses,
        'q': q,
        'course_count': course_count
    }
    return render(request, 'home.html', context=context)


def notification(request):
    user_id = request.user.id if request.user.is_authenticated else None
    notifications = Notification.objects.filter(user=user_id)
    return render(request, 'notification.html', {'user_id': user_id, 'notifications': notifications})
