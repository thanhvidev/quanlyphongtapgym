from django.contrib import admin
from .models import Category, Course, Membership, Review


class MembershipAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'date_joined',
                    'time', 'schedule', 'duration']
    list_filter = ['course']
    search_fields = ['user__email', 'course__name']


class CategoryAdmin(admin.ModelAdmin):  # QUẢN LÝ PHÂN LOẠI
    # Gợi ý trường slug theo category_name
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ('category_name', 'slug')


class CourseAdmin(admin.ModelAdmin):
    list_display = ['id_course', 'name', 'trainer', 'tuition_course', 'created_date', 'is_active', 'quantity_member',
                    'image_course']
    list_filter = ['trainer']
    search_fields = ['name', 'trainer__user__first_name',
                     'trainer__user__last_name']
    prepopulated_fields = {'slug': ('name',)}


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'content', 'review_time']
    list_filter = ['course']
    search_fields = ['user__email', 'course__name']


admin.site.register(Course, CourseAdmin)
admin.site.register(Membership, MembershipAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Category, CategoryAdmin)
