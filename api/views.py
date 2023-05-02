import uuid
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny
from django.http import HttpResponseBadRequest
from django.db import DatabaseError
from core.models import User
from core.models import Profile
from .serializers import UserSerializer
from .serializers import ProfileSerializer
from .serializers import RegisterAccount
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

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
# MOVIE
from rest_framework.decorators import api_view, permission_classes
from core.models import Movie, MovieImage
from .serializers import MovieImageSerializer, MovieSerializer
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponseServerError
import base64




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
    authentication_classes = [SessionAuthentication, BasicAuthentication]
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
        if request.user.is_authenticated:
            Token.objects.filter(user=request.user).delete()
        response = Response({'message': 'Logout success'}, status=status.HTTP_200_OK)
        response.delete_cookie('token')  # remove session cookie
        logout(request) 
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
            user = request.user
            if user.role != 'UserAdmin':
                return Response({'message': 'You don\'t have permission to suspend account'}, status=403)
            # Get the username from the request data
            username = request.data.get('username')
            # Retrieve the user with the specified username 
            user1 = User.objects.get(username=username)
            # Check if the user is already suspended
            if not user1.is_active:
                return Response({'message': 'User account is already suspended.'}, status=status.HTTP_400_BAD_REQUEST)
            # Suspend the user account
            user1.is_active = False
            user1.save()
            # Return a success response
            return Response({'message': 'User account has been suspended.'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    @api_view(['POST'])
    def reactivateUser(request):
        try:
            user = request.user
            if user.role != 'UserAdmin':
                return Response({'message': 'You don\'t have permission to suspend account'}, status=403)
            # Get the username from the request data
            username = request.data.get('username')
            # Retrieve the user with the specified username 
            user1 = User.objects.get(username=username)
            # Check if the user is already suspended
            if user1.is_active:
                return Response({'message': 'User account is not suspended.'}, status=status.HTTP_400_BAD_REQUEST)
            # Suspend the user account
            user1.is_active = True
            user1.save()
            # Return a success response
            return Response({'message': 'User account activated.'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)


    @api_view(['POST'])
    def changePassword(request):
        try:
            user = request.user
            if user.role != 'UserAdmin':
                return Response({'message': 'You don\'t have permission to suspend account'}, status=403)
            # Get the username and new password from the request data
            username = request.data.get('username')
            new_password = request.data.get('new_password')
            # Retrieve the user with the specified username
            user1 = User.objects.get(username=username)
            # Set the new password for the user
            user1.set_password(new_password)
            user1.save()
            # Return a success response
            return Response({'message': 'User password has been changed.'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

    @api_view(['POST'])
    def changeEmail(request):
        try:
            user = request.user
            if user.role != 'UserAdmin':
                return Response({'message': 'You don\'t have permission to suspend account'}, status=403)
            # Get the username and new email from the request data
            username = request.data.get('username')
            new_email = request.data.get('new_email')
            # Retrieve the user with the specified username
            user1 = User.objects.get(username=username)
            # Check if new email is provided
            if not new_email:
                raise ValueError('New email is required')
            # Set the new email for the user
            user1.email = new_email
            user1.save()
            # Return a success response
            return Response({'message': 'User email has been changed.'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

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
    
class movieIMG(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @api_view(['GET'])
    def viewMovieImage(self, request):
        """
        Returns a list of all movie images.
        """
        # Check if user has permission to view movie images
        if request.user.role != 'CinemaManager':
            return Response({'message': 'You don\'t have permission to view movie images'}, status=403)

        movies = MovieImage.objects.all()
        serializer = MovieImageSerializer(movies, many=True)
        return Response(serializer.data)
    
    def getMovieImage(self, request):
        """
        Returns a list of all image objects that match the given movie ID.
        """
        # Check if user has permission to view movie images
        if request.user.role != 'CinemaManager':
            return Response({'message': 'You don\'t have permission to view movie images'}, status=403)

        # Get movie ID from request
        movie_id = request.data.get('id')

        # Get all image objects that match the movie ID
        images = MovieImage.objects.filter(movie_id=movie_id)

        serializer = MovieImageSerializer(images, many=True)
        return Response(serializer.data)

    @api_view(['POST'])
    def addMovieImg(request):
        # Check if user is a cinemaManager
        if request.user.role != 'CinemaManager':
            return Response(status=status.HTTP_403_FORBIDDEN)

        # Get the movie object to add the image to
        movie_id = request.data.get('movie')
        movie = Movie.objects.get(pk=movie_id)

        # Create serializer with data from request body
        serializer = MovieImageSerializer(data=request.data)
        # Validate serializer data
        if serializer.is_valid():
            # Save serializer and return response
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # Return 400 if data is invalid
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class Movies(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    @api_view(['POST'])
    def addMov(request):
        # Check if user is a cinemaManager
        if request.user.role != 'CinemaManager':
            return Response(status=status.HTTP_403_FORBIDDEN)
        # Create serializer with data from request body
        serializer = MovieSerializer(data=request.data)
        
        # Validate serializer data
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # Return 400 if data is invalid
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    @api_view(['POST'])
    def delMov(request):
        # Check if user is a cinemaManager
        if request.user.role != 'CinemaManager':
            return Response(status=status.HTTP_403_FORBIDDEN)

        try:
            # Retrieve the movie with the specified id
            movie_id = request.data.get('id')
            movie = Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            # If the movie does not exist, return 404 error
            return Response({'message': 'Movie not found.'}, status=status.HTTP_400_BAD_REQUEST)

        # Delete the movie from the database
        movie.delete()
        # Return a success response
        return Response({'message': 'Movie deleted successfully.'}, status=status.HTTP_200_OK)
    

class SearchMovie(APIView):
    permission_classes = [AllowAny]

    @api_view(['POST'])
    def SearchMov(request):
        # Retrieve the search keyword from the request body
        keyword = request.data.get('keyword')

        if keyword is not None:
            # Retrieve all movies that match the search keyword
            movies = Movie.objects.filter(movie_title__icontains=keyword)

            # Serialize the movies data
            serializer = MovieSerializer(movies, many=True)

            # Return the serialized movies data as a response
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response("No keyword provided", status=status.HTTP_400_BAD_REQUEST)