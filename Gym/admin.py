from django.contrib import admin
from .models import Notification


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'content', 'is_seen','timestamp')
    list_filter = ('user', 'is_seen')
    search_fields = ('user__username', 'content')


admin.site.register(Notification, NotificationAdmin)
