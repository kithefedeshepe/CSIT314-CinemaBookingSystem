from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile

# Register your models here

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role',)
    list_filter = ('role',)

admin.site.register(User, CustomUserAdmin)

class CustomProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)

admin.site.register(Profile, CustomProfileAdmin)
