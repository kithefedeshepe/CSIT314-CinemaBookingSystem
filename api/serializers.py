#Handle complex data type
from rest_framework import serializers
from core.models import User
from core.models import Profile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
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