from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json


class NotificationConsumer(WebsocketConsumer):

    def connect(self):
        self.room_name = 'notification_consumer'
        self.room_group_name = 'notification_consumer_group'
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        print("Đã kết nối đến nhóm kênh.", self.room_group_name)

    def receive(self, text_data):
        print(text_data)

    def disconnect(self, *args, **kwargs):
        print('Ngắt kết nối')

    def send_notification(self, event):
        content = event['content']
        self.send(text_data=json.dumps(content))
        print("Gửi thông báo: ", content)
