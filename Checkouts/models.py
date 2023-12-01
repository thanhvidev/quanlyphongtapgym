from django.db import models
from Carts.models import CartItem
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.
from Courses.models import Course


class Checkout(models.Model):
    STATUS_CHOICES = [
        ('cho_xac_nhan', 'Chờ xác nhận'),
        ('thanh_cong', 'Thành công'),
    ]
    checkout_id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=100)
    order_id = models.CharField(max_length=100, default='1')
    checkout_Amount = models.IntegerField()
    checkout_Coursename = models.CharField(
        max_length=255, default='Tên khóa học mặc định')
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='chua_xac_nhan',
    )

    def __str__(self):
        return str(self.checkout_id)

    def get_status_display(self):
        return dict(self.STATUS_CHOICES).get(self.status, '')
