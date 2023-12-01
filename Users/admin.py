from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, TrainerProfile


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['id', 'email', 'first_name', 'last_name', 'phonenumber',
                    'gender', 'age', 'avatar', 'join_date', 'is_superuser',
                    'is_trainer', 'is_member', 'is_active', 'password']
    list_filter = ['is_superuser', 'is_trainer', 'is_member']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phonenumber',
                                      'gender', 'age', 'avatar')}),
        ('Permissions', {'fields': ('is_superuser',
         'is_trainer', 'is_member', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_superuser', 'is_trainer', 'is_member'),
        }),
    )
    search_fields = ['email']
    ordering = ['email']
    list_display_links = ['email']

    def get_readonly_fields(self, request, obj=None):
        if obj and obj == request.user:  # Kiểm tra xem người dùng đang chỉnh là người đăng nhập
            # Chỉ đọc trường is_superuser cho chính họ
            return ('email', 'is_superuser',)
        if obj:
            return ('email',)
        return super().get_readonly_fields(request, obj)


class TrainerProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'description', 'experience', 'education', 'skills',
                    'achievements', 'certificates', 'facebook', 'instagram', 'linkedin', 'twitter']
    search_fields = ['user__first_name',
                     'user__last_name']
    list_display_links = ['user']


admin.site.register(TrainerProfile, TrainerProfileAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
