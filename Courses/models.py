import logging
from django.db import models
from Users.models import CustomUser, TrainerProfile
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):  # lớp phân loại
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:  # lớp định nghĩa chữ
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.category_name


class Course(models.Model):
    SCHEDULE_CHOICES = [
        ('thu 2', 'Thứ 2'),
        ('thu 3', 'Thứ 3'),
        ('thu 4', 'Thứ 4'),
        ('thu 5', 'Thứ 5'),
        ('thu 6', 'Thứ 6'),
        ('thu 7', 'Thứ 7'),
        ('chunhat', 'Chủ nhật'),
    ]
    TIME_CHOICES = [
        ('08:00 - 09:00', '08:00 - 09:00'),
        ('09:00 - 10:00', '09:00 - 10:00'),
        ('10:00 - 11:00', '10:00 - 11:00'),
        ('13:30 - 14:30', '13:30 - 14:30'),
        ('14:00 - 15:00', '14:00 - 15:00'),
        ('15:00 - 16:00', '15:00 - 16:00'),
        ('16:00 - 17:00', '16:00 - 17:00'),
        ('17:00 - 18:00', '17:00 - 18:00'),
        ('18:30 - 19:30', '18:30 - 19:30'),
        ('19:00 - 20:00', '19:00 - 20:00'),
        ('20:00 - 21:00', '20:00 - 21:00'),
        ('21:00 - 22:00', '21:00 - 22:00'),
    ]
    DURATION_CHOICES = [
        ('1thang', '1 tháng'),
        ('2thang', '2 tháng'),
        ('3thang', '3 tháng'),
        ('6thang', '6 tháng'),
    ]
    address_course_choices = [
        ('phong101', 'phòng 101'),
        ('phong102', 'phòng 102'),
        ('phong103', 'phòng 103'),
        ('phong104', 'phòng 104'),
        ('phong105', 'phòng 105'),
        ('phong106', 'phòng 106'),
        ('phong107', 'phòng 107'),
        ('phong108', 'phòng 108'),
        ('phong109', 'phòng 109'),
        ('phong110', 'phòng 110'),
    ]

    id_course = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)  # Tên khoá học
    slug = models.SlugField(max_length=200, unique=True, default='')
    trainer = models.ForeignKey(TrainerProfile, on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE)
    image_course = models.ImageField(
        upload_to='course_images/', blank=True, null=True)
    banner_course = models.ImageField(
        upload_to='course_banners/', blank=True, null=True)
    address_course = models.CharField(
        max_length=30, choices=address_course_choices, default='phong101')
    schedule_course = models.CharField(
        max_length=30, choices=SCHEDULE_CHOICES, default='thu 2')
    time_course = models.CharField(
        max_length=50, choices=TIME_CHOICES, default='08:00 - 09:00')
    duration_course = models.CharField(
        max_length=30, choices=DURATION_CHOICES, default='1thang')
    description_course = models.TextField(
        max_length=500, blank=True, null=True)
    tuition_course = models.DecimalField(
        max_digits=10, decimal_places=0, default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    quantity_member = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def get_schedule_display(self):
        return dict(self.SCHEDULE_CHOICES).get(self.schedule_course, '')

    def get_duration_display(self):
        return dict(self.DURATION_CHOICES).get(self.duration_course, '')

    @property
    def ImageURL(self):
        try:
            url = self.image_course.url
        except:
            url = ''
        return url

    @property
    def BannerURL(self):
        try:
            url = self.banner_course.url
        except:
            url = ''
        return url


class Membership(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)
    duration = models.CharField(
        _('Duration'), max_length=40, choices=Course.DURATION_CHOICES)
    schedule = models.CharField(
        _('Schedule'), max_length=40, choices=Course.SCHEDULE_CHOICES)
    time = models.CharField(
        _('Time'), max_length=40, choices=Course.TIME_CHOICES)

    def __str__(self):
        return f'{self.user.email} - {self.course.name}'


class Review(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    membership = models.ForeignKey(Membership, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    rating = models.IntegerField(default=0, validators=[
        MinValueValidator(1),
        MaxValueValidator(5)
    ])
    review_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.email} - {self.course.name}'
