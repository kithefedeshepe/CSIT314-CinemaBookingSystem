#Handle complex data type
from rest_framework import serializers
from core.models import User
from core.models import Profile, Movie, MovieImage, CinemaRoom
from django.http import JsonResponse


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'is_active',
            'role'
        ]

class RegisterAccount(serializers.ModelSerializer):
    #media_type = serializers.CharField(max_length=100)
    #username = serializers.CharField(max_length=50)
    #password = serializers.CharField(max_length=50)
    #email = serializers.EmailField()
    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'email',
            'role',
        ]

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'id',
            'user',
            'name',
            'date_of_birth',
            'loyalty_points',
        ]

class MovieImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieImage
        fields = [
            'data',
            'movie',
        ]

class MovieSerializer(serializers.ModelSerializer):
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
        ]

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
        ]

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