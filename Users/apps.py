from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Users'
    verbose_name = 'Users'

    # Thêm ordering để đặt vị trí của ứng dụng trong trang admin
    def ready(self):
        from django.contrib import admin
        # admin.site.index_template = 'admin/custom_index.html'
        # admin.site.app_index_template = 'admin/custom_app_index.html'
        admin.site.site_title = 'Quản lý phòng tập gym'
        admin.site.site_header = 'Quản lý phòng tập gym'
        admin.site.index_title = 'Dashboard'
        # admin.site.unregister(CustomUser)
        # admin.site.register(Log, CustomUserAdmin)
        admin.autodiscover()

    ordering = ['name']
