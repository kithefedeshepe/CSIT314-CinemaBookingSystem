from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, Profile, Movie, MovieSession, CinemaRoom, Seat
from django.db import models

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('email', 'role')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'is_staff'),
        }),
    )
    list_display = ('username', 'email', 'role', 'is_staff')
    list_filter = ('role',)
    search_fields = ('username', 'email')
    ordering = ('username',)

    def has_module_permission(self, request):
        if request.user.is_superuser:
            return True
        else:
            if not request.user.is_anonymous:
                if request.user.role == 'UserAdmin':
                    return True
        return False

class ProfileAdmin(admin.ModelAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role'),
        }),
    )
       
    list_display = ('user', 'name', 'date_of_birth', 'loyalty_points')
    list_filter = ('user__role',)
    search_fields = ('user__username', 'name')
    ordering = ('user__username',)

    def has_module_permission(self, request):
        if request.user.is_superuser:
            return True
        else:
            if not request.user.is_anonymous:
                if request.user.role == 'CinemaManager':
                    return False
                if request.user.role == 'UserAdmin':
                    return True
        return False

class MovieAdmin(admin.ModelAdmin):
    list_display = ('poster', 'movie_title', 'genre', 'formatted_duration', 'release_date')
    list_filter = ('genre', 'release_date')
    search_fields = ('movie_title', 'genre')
    ordering = ('movie_title',)
    
class MovieSessionAdmin(admin.ModelAdmin):
    list_display = ('movie', 'session_date', 'session_time', 'cinema_room')
    list_filter = ('movie', 'session_date', 'session_time')
    search_fields = ('movie', 'session_date', 'session_time')
    ordering = ('movie',)

    
class CinemaRoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity')
    list_filter = ('name', 'capacity')
    search_fields = ('name',)
    ordering = ('name',)
    
class SeatAdmin(admin.ModelAdmin):
    list_display = ('movie_session', 'row_number', 'seat_number')
    list_filter = ('movie_session', )
    search_fields = ('movie_session',)
    ordering = ('movie_session',)   
    
admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(MovieSession, MovieSessionAdmin)
admin.site.register(CinemaRoom, CinemaRoomAdmin)
admin.site.register(Seat, SeatAdmin)