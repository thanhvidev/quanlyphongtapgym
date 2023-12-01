from rest_framework import viewsets
from Checkouts.models import Checkout

from Courses.views import courses
from .models import CustomUser
from .serializers import CustomUserSerializer
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .forms import RegisterForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from .tokens import account_activation_token
from django.shortcuts import render
from rest_framework import viewsets
from .models import TrainerProfile
from .serializers import TrainerProfileSerializer
from django.contrib.auth.decorators import login_required
from .forms import AvatarUploadForm


class TrainerProfileViewSet(viewsets.ModelViewSet):
    queryset = TrainerProfile.objects.all()
    serializer_class = TrainerProfileSerializer


def activate(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        print(f"The decoded UID is: {uid}")
        user = CustomUser.objects.get(pk=uid)
        print(f"The corresponding user exists.")
        # Thêm dòng in để kiểm tra giá trị của uid và token
        print(f"uid: {uid}, token: {token}")

        if not user.is_active:
            user.is_active = True
            user.save()
            messages.success(
                request, "Tài khoản của bạn đã được kích hoạt. Vui lòng đăng nhập.", extra_tags='register_success')
        else:
            messages.warning(
                request, "Tài khoản đã được kích hoạt trước đó.", extra_tags='register_warning')
    except Exception as e:
        messages.error(request, "Có lỗi xảy ra.", extra_tags='register_error')
    return redirect('login')


def activateEmail(request, user, to_email):
    mail_subject = 'Kích hoạt tài khoản'
    message = render_to_string('emailAuth.html', {
        'user': user,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email_sent = send_mail(mail_subject, message,
                           'hoaivi2107@gmail.com', [to_email])
    if email_sent:
        messages.success(request, "", extra_tags='register_success')
    else:
        messages.error(
            request, "Có lỗi xảy ra trong quá trình gửi email", extra_tags='register_error')


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            messages.success(
                request, "Bạn đã đăng ký thành công, vui lòng kiểm tra email để kích hoạt tài khoản", extra_tags='register_success')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


class CustomUserViewSet(viewsets.ModelViewSet):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(serializer.validated_data.get('password'))
        user.save()


def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin:index')
        elif request.user.is_trainer or request.user.is_member:
            return redirect('home')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if user.is_superuser:
                        return redirect('admin:index')
                    elif user.is_trainer or user.is_member:
                        return redirect('home')
                else:
                    messages.error(
                        request, "Tài khoản của bạn chưa được kích hoạt.")
            else:
                form.add_error(None, 'Email hoặc mật khẩu không đúng.')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


def profile_view(request):
    return render(request, 'profile.html')


def change_avatar(request):
    if request.method == 'POST':
        form = AvatarUploadForm(request.POST, request.FILES)
        if form.is_valid():
            user = request.user
            user.avatar = form.cleaned_data['avatar']
            user.save()
            # Chuyển hướng người dùng đến trang profile sau khi cập nhật ảnh đại diện
            return redirect('profile')
    else:
        form = AvatarUploadForm()

    return render(request, 'profile.html', {'form': form})


def course_purchased(request):
    user_id = request.user.id
    checkouts = Checkout.objects.filter(user_id=user_id)
    return render(request, 'course_purchased.html', {'checkouts': checkouts})


def schedule(request):
    return render(request, 'schedule.html')
