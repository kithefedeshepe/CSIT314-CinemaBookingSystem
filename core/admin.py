from django.contrib import admin
from .models import User, Profile

class ProfileAdmin(admin.ModelAdmin):
    pass

    class Meta:
        model = Profile

admin.site.register(User)
admin.site.register(Profile, ProfileAdmin)