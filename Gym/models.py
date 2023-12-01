from django.db import models
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.dispatch import receiver
from Courses.models import Course, Membership
from Users.models import CustomUser
import json


class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    content = models.TextField(max_length=500, default='')
    timestamp = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        channels_layer = get_channel_layer()
        notification_objs = Notification.objects.filter(
            user=self.user, course=self.course, is_seen=False).count()
        data = self.content
        print(f"Gửi dữ liệu: {data}")
        async_to_sync(channels_layer.group_send)(
            'notification_consumer_group', {
                'type': 'send_notification',
                'content': json.dumps(data)
            }
        )
        super(Notification, self).save(*args, **kwargs)


# class Notification(models.Model):
#     id = models.AutoField(primary_key=True)
#     sender = models.ForeignKey(TrainerProfile, on_delete=models.CASCADE)
#     recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     course = models.ForeignKey(Course, on_delete=models.CASCADE)
#     content = models.TextField()  # Nội dung thông báo
#     date_sent = models.DateTimeField(auto_now_add=True)  # Ngày gửi
#     is_read = models.BooleanField(default=False)  # Đánh dấu đã đọc hay chưa

#     def __str__(self):
#         return f'Thông báo {self.id}'

# class Schedule(models.Model):
#     id = models.AutoField(primary_key=True)
#     member = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     trainer = models.ForeignKey(TrainerProfile, on_delete=models.CASCADE)
#     course = models.ForeignKey(Course, on_delete=models.CASCADE)

#     def __str__(self):
#         return f'Schedule {self.id}'
