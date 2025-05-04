from django.contrib import admin
from django.utils.html import format_html
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_modaretor', 'display_profile_image')
    list_filter = ('is_modaretor', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    readonly_fields = ('display_profile_image',)
    fieldsets = (
        ('User Information', {
            'fields': ('username', 'email', 'first_name', 'last_name', 'profile_images', 'display_profile_image')
        }),
        ('Permissions', {
            'fields': ('is_modaretor', 'is_staff', 'is_active')
        }),
    )

    def display_profile_image(self, obj):
        if obj.profile_images:
            return format_html('<img src="{}" width="100" height="100" style="border-radius: 50%;" />', obj.profile_images.url)
        return "No image"
    display_profile_image.short_description = 'Profile Image Preview'

admin.site.register(CustomUser, CustomUserAdmin)
