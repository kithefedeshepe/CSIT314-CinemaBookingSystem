from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny
from django.db import DatabaseError
from core.models import User
from .serializers import UserSerializer
from .serializers import RegisterAccount
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
# Create your views here.
# LOGIN 
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework import status
# LOGOUT
from django.contrib.auth import logout
from rest_framework.response import Response
# UPDATE
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from core.models import CustomUserManager



class AccountController:
    @api_view(['GET'])
    def getUserAccount(request):
        user_account = User.objects.all()
        serializer = UserSerializer(user_account, many = True)
        return Response(serializer.data)

    @api_view(['POST'])
    def RegisterAccount(request):
        try:
            # Encrypt the password before passing it to the serializer instance
            password = request.data.get('password')
            encrypted_password = make_password(password)

            # Pass data with encrypted password to the serializer instance
            data = request.data.copy()
            data['password'] = encrypted_password
            serializer = RegisterAccount(data=data)

            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)

            return Response({"invalid": "bad data"}, status=400)
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
            response.set_cookie('token', token.key)  # add session cookie
            return response
        else:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        if not request.user.is_authenticated:
            raise PermissionDenied()
        response = Response({'message': 'Logout success'}, status=status.HTTP_200_OK)
        logout(request)
        response.delete_cookie('token')  # remove session cookie
        if request.user.is_authenticated:
            Token.objects.filter(user=request.user).delete()
        return response
    
class GetUserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        user_data = {
            'id': user.id,
            'username': user.username,
            'role': user.role
        }
        return Response(user_data, status=status.HTTP_200_OK)
    
#4 functions
class UpdateUser(APIView):
    #authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def suspendUser(self, request):
        try:
            # Check if user has permission to suspend accounts
            if request.user.role != 'UserAdmin':
                raise PermissionDenied("You do not have permission to suspend accounts.")
            # Get the username from the request data
            username = request.data.get('username')
            # Retrieve the user with the specified username
            user = User.objects.get(username=username)
            # Check if the user is already suspended
            if not user.is_active:
                return Response({'message': 'User account is already suspended.'}, status=status.HTTP_400_BAD_REQUEST)
            # Suspend the user account
            user.is_active = False
            user.save()
            # Return a success response
            return Response({'message': 'User account has been suspended.'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def reactivateUser(self, request):
        try:
            # Check if user has permission to reactivate accounts
            if request.user.role != 'UserAdmin':
                raise PermissionDenied("You do not have permission to reactivate accounts.")
            # Get the username from the request data
            username = request.data.get('username')
            # Retrieve the user with the specified username
            user = User.objects.get(username=username)
            # Reactivate the user account
            user.is_active = True
            user.save()
            # Return a success response
            return Response({'message': 'User account has been reactivated.'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def changePassword(self, request):
        try:
            # Check if user has permission to change passwords
            if request.user.role != 'UserAdmin':
                raise PermissionDenied("You do not have permission to change passwords.")
            # Get the username and new password from the request data
            username = request.data.get('username')
            new_password = request.data.get('new_password')
            # Retrieve the user with the specified username
            user = User.objects.get(username=username)
            # Set the new password for the user
            user.set_password(new_password)
            user.save()
            # Return a success response
            return Response({'message': 'User password has been changed.'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def changeEmail(self, request):
        try:
            # Check if user has permission to change email
            if request.user.role != 'UserAdmin':
                raise PermissionDenied("You do not have permission to change email.")
            # Get the username and new email from the request data
            username = request.data.get('username')
            new_email = request.data.get('new_email')
            # Retrieve the user with the specified username
            user = User.objects.get(username=username)
            # Check if new email is provided
            if not new_email:
                raise ValueError('New email is required')
            # Set the new email for the user
            user.email = new_email
            user.save()
            # Return a success response
            return Response({'message': 'User email has been changed.'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
