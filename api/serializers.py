#Handle complex data type
from rest_framework import serializers
from core.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'role'
        ]

class RegisterAccount(serializers.Serializer):
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
