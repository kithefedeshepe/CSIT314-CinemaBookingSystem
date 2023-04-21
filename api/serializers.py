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
