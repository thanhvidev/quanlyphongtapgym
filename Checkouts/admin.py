from django.contrib import admin
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from Courses.models import Course, Membership
from .models import Checkout
from django.core.mail import send_mail
from Users.models import CustomUser


class CheckoutAdmin(admin.ModelAdmin):
    list_display = ['checkout_id', 'order_id', 'user_id', 'checkout_Coursename',
                    'checkout_Amount', 'created_date', 'status']
    list_filter = ['status', 'created_date', 'user_id']
    list_editable = ['status']

    def save_model(self, request, obj, form, change):
        if change:
            user_id = obj.user_id
            course_names = obj.checkout_Coursename.split(',')
            for course_name in course_names:
                course = get_object_or_404(Course, name=course_name.strip())

                if obj.status == 'thanh_cong':
                    membership = Membership.objects.create(
                        user_id=user_id, course=course)
                    membership.time = course.time_course
                    membership.schedule = course.schedule_course
                    membership.duration = course.duration_course
                    membership.save()

                    # Gửi email xác nhận thanh toán
                    subject = 'Xác nhận thanh toán thành công'
                    message = f'Chào mừng bạn đến với khóa học {course_name.strip()}!'
                    from_email = 'hoaivi2107@email.com'
                    custom_user = CustomUser.objects.get(id=user_id)
                    to_email = [custom_user.email]
                    send_mail(subject, message, from_email,
                              to_email, fail_silently=False)

                elif obj.status == 'cho_xac_nhan':
                    Membership.objects.filter(
                        user_id=user_id, course=course).delete()

        super().save_model(request, obj, form, change)


admin.site.register(Checkout, CheckoutAdmin)


@receiver(post_delete, sender=Checkout)
def delete_membership_on_checkout_delete(sender, instance, **kwargs):

    user_id = instance.user_id
    course_names = instance.checkout_Coursename.split(',')

    for course_name in course_names:
        course = get_object_or_404(Course, name=course_name.strip())
        Membership.objects.filter(user_id=user_id, course=course).delete()
