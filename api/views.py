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
from .serializers import UserSerializer, UpdateMovieSerializer
from .serializers import ProfileSerializer
from .serializers import RegisterAccount
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.utils import timezone

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
from core.models import Movie, CinemaRoom, FoodandBeverage, MovieSession
from .serializers import MovieSerializer, CinemaRoomSerializer, FoodandBeverageSerializer, MovieSessionSerializer
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponseServerError
import base64
from django.core.exceptions import ValidationError
from datetime import datetime
# PURCHASE BOOKING
from .serializers import PurchaseTicketSerializer
from core.models import PurchaseTicket


class AccountController:
    #GETS USER ACCOUNT
    @api_view(['GET'])
    def getUserAccount(request):
        user_account = User.objects.all()
        serializer = UserSerializer(user_account, many = True)
        return Response(serializer.data)

    #REGISTERS ACCOUNT PARAMETER: PW
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

    #LOGIN(username, pw) 
    @api_view(['POST'])
    def login(request):
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

    #LOGOUT()
    @api_view(['POST'])
    def logout(request):
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

    #getUser(id, username, role)
    @api_view(['GET'])
    def getUser(request):
        user = request.user
        user_data = {
            'id': user.id,
            'username': user.username,
            'role': user.role
        }
        return Response(user_data, status=status.HTTP_200_OK)
    
class UpdateUser(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    #suspendUser(username)
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
    
    @api_view(['POST'])
    def getProfile(request):
        myusername = request.data.get('username')
        profile = Profile.objects.get(user__username=myusername)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
    
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
            movie_title_obj = request.data.get('movie_title')
            movie = Movie.objects.get(movie_title=movie_title_obj)
        except Movie.DoesNotExist:
            # If the movie does not exist, return 404 error
            return Response({'message': 'Movie not found.'}, status=status.HTTP_400_BAD_REQUEST)

        # Delete the movie from the database
        movie.delete()
        # Return a success response
        return Response({'message': 'Movie deleted successfully.'}, status=status.HTTP_200_OK)
    
    @api_view(['POST'])    
    def updateMov(request):
        
        # Check if user is a cinemaManager.
        if request.user.role != 'CinemaManager':
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        # Get the movie object to update
        movie_tile_obj = request.data.get('movie_title')
        try:
            movie = Movie.objects.get(movie_title=movie_tile_obj)
        except Movie.DoesNotExist:
            return Response({'message': 'Movie does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        # Create serializer with data from request body
        serializer = MovieSerializer(movie, data=request.data, partial=True)

        # Validate serializer data
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # Return 400 if data is invalid
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    @api_view(['POST'])
    def addCR(request):
        # Check if user is a cinemaManager.
        if request.user.role != 'CinemaManager':
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        serializer = CinemaRoomSerializer(data=request.data)
        # Validate serializer data
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # Return 400 if data is invalid
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET'])   
    def viewAllCR(request):
        # Check if user is a cinemaManager.
        if request.user.role != 'CinemaManager':
            #return Response(status=status.HTTP_403_FORBIDDEN)
            cinemaRooms = CinemaRoom.objects.all()
            serializer = CinemaRoomSerializer(cinemaRooms, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
    @api_view(['POST'])
    def updateCR(request):
        # Check if user is a cinemaManager.
        if request.user.role != 'CinemaManager':
            return Response(status=status.HTTP_403_FORBIDDEN)

        # Get the movie object to update
        roomName = request.data.get('name')
        try:
            cinemaRoom = CinemaRoom.objects.get(name=roomName)
        except CinemaRoom.DoesNotExist:
            return Response({'message': 'Cinema Room does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        # Create serializer with data from request body
        serializer = CinemaRoomSerializer(cinemaRoom, data=request.data, partial=True)

        # Validate serializer data
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=400)
        
    @api_view(['POST'])
    def delCR(request):
         # Check if user is a cinemaManager.
        if request.user.role != 'CinemaManager':
            return Response(status=status.HTTP_403_FORBIDDEN)

        # Get the cinema room object to delete
        roomName = request.data.get('name')
        try:
            cinemaRoom = CinemaRoom.objects.get(name=roomName)
        except CinemaRoom.DoesNotExist:
            return Response({'message': 'Cinema Room does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        # Delete the cinema room
        cinemaRoom.delete()
        return Response(status=status.HTTP_200_OK)
    
    @api_view(['GET'])   
    def viewAllCR(request):
        # Check if user is a cinemaManager.
        if request.user.role != 'CinemaManager':
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        cinemaRooms = CinemaRoom.objects.all()
        serializer = CinemaRoomSerializer(cinemaRooms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    @api_view(['POST'])
    def addMS(request):
        # Check if user is a cinemaManager.
        if request.user.role != 'CinemaManager':
            return Response(status=status.HTTP_403_FORBIDDEN)

        # Get movie, session date, cinema room and session time from request data
        try:
            title = request.data['movie_title']
            session_date = request.data['session_date']
            cinema_room_name = request.data['cinema_room']
            session_time = request.data['session_time']
        except (KeyError, ValueError):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # Retrieve movie and cinema room objects from the database
        try:
            movie = Movie.objects.get(movie_title=title)
            cinema_room = CinemaRoom.objects.get(name=cinema_room_name)
        except (Movie.DoesNotExist, CinemaRoom.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Check if session time is valid
        valid_session_times = ['8:30', '11:30', '14:00', '16:30', '17:50', '18:40', '19:30', '20:40', '21:10']
        if session_time not in valid_session_times:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # Create new movie session
        movie_session = MovieSession.objects.create(
            movie=movie,
            session_date=session_date,
            cinema_room=cinema_room,
            session_time=session_time
        )

        return Response(status=status.HTTP_200_OK)
    
    @api_view(['GET'])
    def viewAllMS(request):
        # Check if user is a cinemaManager.
        if request.user.role != 'CinemaManager':
            return Response(status=status.HTTP_403_FORBIDDEN)

        # Retrieve all movie sessions from the database
        movie_sessions = MovieSession.objects.all()

        # Serialize the movie sessions
        serializer = MovieSessionSerializer(movie_sessions, many=True)

        # Return the serialized data
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @api_view(['POST'])
    #Search by movie session id
    def delMS(request):
        # Check if user is a cinemaManager.
        if request.user.role != 'CinemaManager':
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        try:
            myid = request.data['id']
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            session = MovieSession.objects.filter(id=myid)
            if not session:
                raise MovieSession.DoesNotExist
        except MovieSession.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        session.delete()
        return Response(status=status.HTTP_200_OK)
    
    @api_view(['POST'])
    def getMovieSession(request):
        try:
            movie_title = request.data['movie']
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            movie = Movie.objects.get(movie_title=movie_title)
            sessions = MovieSession.objects.filter(movie=movie)
        except (Movie.DoesNotExist, CinemaRoom.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)

        serialized_sessions = MovieSessionSerializer(sessions, many=True).data
        return Response(serialized_sessions, status=status.HTTP_200_OK)
        

class allowAnyMovie(APIView):
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
        
    @api_view(['GET'])
    def viewAllMovie(request):
        """
        Returns a list of all movie images
        """
        movies = Movie.objects.all()
        serializer = UpdateMovieSerializer(movies, many=True)
        return Response(serializer.data)
    
    #helper function
    @api_view(['GET'])
    def getUpComing(request):
        current_date = timezone.now().date()
        movies = Movie.objects.filter(release_date__gte=current_date)
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

    @api_view(['GET'])
    def getNowShowing(request):
        current_date = timezone.now().date()
        movies = Movie.objects.filter(release_date__lt=current_date)
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)
    

class Fnbs(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    @api_view(['POST'])
    def addFnb(request):
         #Check if user is a cinemaManager.
        if request.user.role != 'CinemaManager':
            return Response(status=status.HTTP_403_FORBIDDEN)

        # Create serializer with data from request body
        serializer = FoodandBeverageSerializer(data=request.data)

        # Validate serializer data
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    @api_view(['GET'])
    def viewAllFnb(request):
         # Get all FnBs
        fnbs = FoodandBeverage.objects.all()

        # Serialize the queryset
        serializer = FoodandBeverageSerializer(fnbs, many=True)

        # Return the serialized data
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @api_view(['POST'])
    def updateFnB(request):
        # Check if user is a cinemaManager.
        if request.user.role != 'CinemaManager':
            return Response(status=status.HTTP_403_FORBIDDEN)

        # Get the FnB to update
        try:
            fnb = FoodandBeverage.objects.get(menu=request.data['menu'])
        except FoodandBeverage.DoesNotExist:
            return Response({'message': 'FnB not found'}, status=status.HTTP_404_NOT_FOUND)

        # Update the FnB data
        serializer = FoodandBeverageSerializer(fnb, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    @api_view(['POST'])
    def delFnB(request):
        # Check if user is a cinemaManager.
        if request.user.role != 'CinemaManager':
            return Response(status=status.HTTP_403_FORBIDDEN)

        # Get the FnB to delete
        try:
            fnb = FoodandBeverage.objects.get(menu=request.data['menu'])
        except FoodandBeverage.DoesNotExist:
            return Response({'message': 'FnB not found'}, status=status.HTTP_404_NOT_FOUND)

        # Delete the FnB
        fnb.delete()
        return Response(status=status.HTTP_200_OK)

class Purchase(APIView):
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]

    #still testing
    @api_view(['POST'])
    def addBook(request):
        try:
            username = request.data['booking_owner']
            session_id = request.data['movie_session']
            ticket_type = request.data['ticket_type']
            seat_number = request.data['seat_number']
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=username)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            session = MovieSession.objects.get(id=session_id)
        except MovieSession.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        booking = PurchaseTicket.objects.create(
            booking_owner=user,
            movie_session=session,
            ticket_type=ticket_type,
            seat_number=seat_number
        )

        return Response(status=status.HTTP_200_OK)

    #still testing
    #@api_view(['POST']) 
    @api_view(['GET'])
    def viewAllBook(request):
        # Check if user is authenticated.
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        #try:
        #    username = request.data['booking_owner']
        #except KeyError:
        #    return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            #bookings = PurchaseTicket.objects.filter(booking_owner=username)
            bookings = PurchaseTicket.objects.filter(booking_owner=request.user)
        except PurchaseTicket.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = PurchaseTicketSerializer(bookings, many=True)
        return Response(serializer.data)