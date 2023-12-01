from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from Courses.forms import ReviewForm
from .models import Category, Course, Membership, Review
from .serializers import CourseSerializer
from django.shortcuts import render, get_object_or_404, redirect


def courses(request):
    courses = Course.objects.all()
    context = {'courses': courses}
    return render(request, 'course.html', context)


def course_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    courses = Course.objects.filter(is_active=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        courses = courses.filter(category=category)
    context = {
        'category': category,
        'categories': categories,
        'products': courses
    }
    return render(request, 'course_list.html', context)


def course_detail(request, category_slug, course_slug):
    course = Course.objects.get(category__slug=category_slug, slug=course_slug)
    reviews = Review.objects.filter(course=course)

    # Kiểm tra xem người dùng có membership cho khoá học hay không (nếu đã đăng nhập)
    has_membership = False
    if request.user.is_authenticated:
        has_membership = Membership.objects.filter(
            user=request.user, course=course).exists()

    has_review = False
    review = None

    if request.user.is_authenticated:
        try:
            # Lấy đánh giá nếu tồn tại
            review = Review.objects.get(user=request.user, course=course)
            has_review = True
        except Review.DoesNotExist:
            pass

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            if has_membership:
                if review:
                    review.content = form.cleaned_data['content']
                    review.rating = form.cleaned_data['rating']
                    review.save()
                else:
                    Review.objects.create(
                        user=request.user,
                        course=course,
                        membership=Membership.objects.get(
                            user=request.user, course=course),
                        content=form.cleaned_data['content'],
                        rating=form.cleaned_data['rating']
                    )
                return redirect('home')
    else:
        form = ReviewForm()

    return render(request, 'course_detail.html', {'course': course, 'review': review, 'reviews': reviews, 'has_review': has_review, 'form': form, 'has_membership': has_membership})


# def course_detail(request, category_slug, course_slug):
#     course = Course.objects.get(
#         category__slug=category_slug, slug=course_slug)
#     reviews = Review.objects.filter(course=course)
#     # Kiểm tra xem người dùng có membership cho khoá học hay không
#     has_membership = Membership.objects.filter(
#         user=request.user, course=course).exists()
#     has_review = Review.objects.filter(
#         user=request.user, course=course).exists()
#     review = None
#     if request.user.is_authenticated:
#         try:
#             # Lấy đánh giá nếu tồn tại
#             review = Review.objects.get(user=request.user, course=course)
#         except Review.DoesNotExist:
#             pass

#     if request.method == 'POST':
#         form = ReviewForm(request.POST)
#         if form.is_valid():
#             if has_membership:
#                 if review:
#                     review.content = form.cleaned_data['content']
#                     review.rating = form.cleaned_data['rating']
#                     review.save()
#                 else:
#                     Review.objects.create(
#                         user=request.user,
#                         course=course,
#                         membership=Membership.objects.get(
#                             user=request.user, course=course),
#                         content=form.cleaned_data['content'],
#                         rating=form.cleaned_data['rating']
#                     )
#                 return redirect('home')
#     else:
#         form = ReviewForm()

#     return render(request, 'course_detail.html', {'course': course, 'review': review, 'reviews': reviews, 'has_review': has_review, 'form': form, 'has_membership': has_membership})


def courses_by_schedule(request):
    courses_thu2 = Course.objects.filter(schedule_course='thu 2')
    courses_thu3 = Course.objects.filter(schedule_course='thu 3')
    courses_thu4 = Course.objects.filter(schedule_course='thu 4')
    courses_thu5 = Course.objects.filter(schedule_course='thu 5')
    courses_thu6 = Course.objects.filter(schedule_course='thu 6')
    courses_thu7 = Course.objects.filter(schedule_course='thu 7')
    courses_chunhat = Course.objects.filter(schedule_course='chunhat')

    context = {
        'courses_thu2': courses_thu2,
        'courses_thu3': courses_thu3,
        'courses_thu4': courses_thu4,
        'courses_thu5': courses_thu5,
        'courses_thu6': courses_thu6,
        'courses_thu7': courses_thu7,
        'courses_chunhat': courses_chunhat,
    }

    return render(request, 'home.html', context)


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
