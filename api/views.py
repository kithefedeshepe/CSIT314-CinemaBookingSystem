from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny
from django.db import DatabaseError
from core.models import User
from core.models import Profile
from .serializers import UserSerializer
from .serializers import ProfileSerializer
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
#Cinema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseServerError
import base64
from core.models import Movie
from .serializers import MovieImageSerializer



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
            if not password:
                return Response({"error": "Password cannot be empty"}, status=400)
            encrypted_password = make_password(password)

            # Pass data with encrypted password to the serializer instance
            data = request.data.copy()
            data['password'] = encrypted_password
            serializer = RegisterAccount(data=data)

            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=200)

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
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @api_view(['POST'])
    def suspendUser(request):
        try:
            # Check if user has permission to suspend accounts
            if request.user.role != 'UserAdmin':
                return Response({'message': 'You don\'t have permission to suspend account'}, status=403)
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
    
    @api_view(['POST'])
    def reactivateUser(request):
        try:
            # Check if user has permission to reactivate accounts
            if request.user.role != 'UserAdmin':
                return Response({'message': 'You don\'t have permission to reactivate account'}, status=403)
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


    @api_view(['POST'])
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

    @api_view(['POST'])
    def changeEmail(request):
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

class SearchUserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @api_view(['POST'])
    def searchUser(request):
         # Check if user has permission to search user
        if request.user.role != 'UserAdmin':
            raise PermissionDenied("You do not have permission to search user.")
        # Get prompt from request body
        prompt = request.data.get('keyword', '')
        # Filter accounts based on the prompt
        accounts = User.objects.filter(username__icontains=prompt)
        # Serialize the accounts to JSON and return a Response object
        serializer = UserSerializer(accounts, many=True)
        return Response(serializer.data)
    
class UserProfile(APIView):
    Authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @api_view(['POST'])
    def createProfile(request):
        # Get the user data from the request
        username = request.data.get('username')
        name = request.data.get('name')
        date_of_birth = request.data.get('date_of_birth')

        # Create the user profile
        user = User.objects.get(username=username)
        profile = Profile.objects.create(user=user, name=name, date_of_birth=date_of_birth)

        # Return a response with the created profile data
        return Response({
            'id': profile.id,
            'user': profile.user.username,
            'name': profile.name,
            'date_of_birth': profile.date_of_birth,
            'loyalty_points': profile.loyalty_points
        }, status=status.HTTP_201_CREATED)
    
    @api_view(['GET'])
    def viewProfile(request):
        # check if user has permission to view profiles
        if request.user.role != 'UserAdmin' and not request.user.is_superuser:
            raise PermissionDenied("You do not have permission to view profiles.")

        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many = True)
        return Response(serializer.data)
    
    @api_view(['GET'])
    def getProfile(request):
        token = request.data.get('token')
        profile = request.user.profiles.first() # retrieve the first profile associated with the user
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
    
class MovieImage(APIView):
        Authentication_classes = [TokenAuthentication]
        permission_classes = [IsAuthenticated]
        @api_view(['POST'])
        def addMovieImage( request):
            if not request.user.role == 'cinemaManager':
                return HttpResponse(status=403)

            # Get movie id and image data from request data
            movie_id = request.data.get('id')
            img_data = request.data.get('data')

            # Check if movie with given id exists
            try:
                movie = MovieImage.objects.get(pk=movie_id)
            except MovieImage.DoesNotExist:
                return HttpResponseNotFound()

            # Convert image data from base64 string to binary data
            try:
                img_binary = base64.b64decode(img_data)
            except:
                return HttpResponseBadRequest()

            # Update movie image field with binary image data
            try:
                movie.image.save(f'{movie_id}.jpg', img_binary)
                movie.save()
            except:
                return HttpResponseServerError()

            # Return serialized movie object with updated image
            serializer = MovieImageSerializer(movie)
            return Response(serializer.data)