#Handle complex data type
from rest_framework import serializers
from core.models import User
from core.models import Profile, Movie, CinemaRoom, FoodandBeverage, MovieSession, MovieBooking
from django.http import JsonResponse

# Serializer: Convert model to json format

# User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'is_active',
            'role'
        ]

# Required field for register account
class RegisterAccount(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'email',
            'role',
        ]

# User profile
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

# Movie
class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = [
            'id',
            'movie_title',
            'genre',
            'duration',
            'release_date',
            'cast',
            'director',
            'movie_description',
            'posterIMG',
            'featureIMG',
        ]

# Update movie
class UpdateMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = [
            'movie_title',
            'genre',
            'duration',
            'release_date',
            'cast',
            'director',
            'movie_description',
            'posterIMG',
            'featureIMG',
        ]

# Cinemaroom
class CinemaRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = CinemaRoom
        fields =[
            'name',
            'capacity'
        ]

    def validate_capacity(self, value):
        if value < 1:
            raise serializers.ValidationError("Capacity must be a positive integer.")
        return value

# Movie session
class MovieSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieSession
        fields = ['id', 
                  'movie', 
                  'session_date', 
                  'cinema_room', 
                  'session_time'
        ]

# Fnb
class FoodandBeverageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodandBeverage
        fields = [
            'id', 
            'menu',
            'menu_description',
            'price',
            'menuIMG'
        ]

# Purchase booking
class PurchaseTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieBooking
        fields = ['id', 
                  'booking_owner', 
                  'movie_session', 
                  'ticket_type', 
                  'seat_number'
        ]
