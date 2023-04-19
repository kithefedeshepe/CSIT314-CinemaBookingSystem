from django.contrib import admin
from .models import User, UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    pass

admin.site.register(User)
admin.site.register(UserProfile, UserProfileAdmin)