from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile

class UserProfileInline(admin.TabularInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Perfiles de Usuario'

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'user__email', 'phone')