from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from django.db import DatabaseError
from core.models import User
from .serializers import UserSerializer
from .serializers import RegisterAccount
from rest_framework.permissions import IsAuthenticated
# Create your views here.
# LOGIN 
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework import status
# LOGOUT
from django.contrib.auth import logout
from rest_framework.response import Response


class AccountController:
    @api_view(['GET'])
    def getUserAccount(request):
        user_account = User.objects.all()
        serializer = UserSerializer(user_account, many = True)
        return Response(serializer.data)

    @api_view(['POST'])
    def RegisterAccount(request):
        try:
            serializer = UserSerializer(request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
            return Response({"invalid": "bad data"}, status = 400)
        except DatabaseError as e:
            return Response({"error": "Bad data"}, status=500)
        
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
            response_data = {
                'message': 'Login success',
                'token': token.key
            }
            response = Response(response_data, status=status.HTTP_200_OK)
            return response
        else:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
class LogoutView(APIView):
    def post(self, request):
        logout(request)
        session_key = request.session.session_key
        if session_key:
            request.session.delete(session_key)
        response = Response({'message': 'Logout success'}, status=status.HTTP_200_OK)
        response.delete_cookie('sessionid')
        return response
    
class GetUserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]
    def get(self, request):
        user = request.user
        user_data = {
            'id': user.id,
            'username': user.username,
            'role': user.role
        }
        return Response(user_data, status=status.HTTP_200_OK)
    
    