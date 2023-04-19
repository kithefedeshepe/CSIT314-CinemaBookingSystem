from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import make_password
from core.models import User
from .serializers import UserSerializer
# Create your views here.

class AccountController:
    @api_view(['GET'])
    def getUserAccount(request):
        user_account = User.objects.all()
        serializer = UserSerializer(user_account, many = True)
        return Response(serializer.data)

    @api_view(['POST'])
    def RegisterAccount(request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)