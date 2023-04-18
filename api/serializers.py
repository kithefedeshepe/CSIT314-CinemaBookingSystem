#Handle complex data type
from rest_framework import serializers
from core.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
        """
        fields = [
            'username',
            'password',
            'role',
        ]
        """