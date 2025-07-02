from django.contrib import admin
from .models import Signup , DoctorProfile
from django.utils.html import mark_safe 

class SignupAdmin(admin.ModelAdmin):
    list_display = ['user', 'gender', 'address', 'birthdate', 'age', 'is_pending']
    list_filter = ['is_pending']
    search_fields = ['user__username', 'address']

    def user_display(self, obj):
        return obj.user.username

admin.site.register(Signup, SignupAdmin)


class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'display_image']
    search_fields = ['user__username']
    def display_image(self, obj):
        if obj.profile_image:
            return mark_safe('<img src="{}" width="50" />'.format(obj.profile_image.url))
        else:
            return 'No Image'

    display_image.short_description = 'Image Preview'

admin.site.register(DoctorProfile, DoctorProfileAdmin)