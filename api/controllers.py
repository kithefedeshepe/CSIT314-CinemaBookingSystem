from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from django.db import DatabaseError
from django.http import JsonResponse
from core.models import User
from core.models import Profile
from .serializers import UserSerializer, UpdateMovieSerializer
from .serializers import ProfileSerializer
from .serializers import RegisterAccount
from rest_framework.permissions import IsAuthenticated
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
from django.core.exceptions import ValidationError
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
            username = request.data.get('username')
            password = request.data.get('password')
            email = request.data.get('email')
            role = request.data.get('role')
            if not password:
                return Response({"error": "Password cannot be empty"}, status=400)
            if not role:
                role = 'Customer'
            user = User()
            user.usercreate(username, password, email, role)
            return Response(status=status.HTTP_200_OK)
        except DatabaseError as e:
            return Response({"error": "Bad data"}, status=500)

        
class LoginView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    #LOGIN(username, pw) 
    @api_view(['POST'])
    def login(request):
        username = request.data.get('username')
        password = request.data.get('password')
        myuser = User()
        token = myuser.userauthenticate(request, username, password)
        if token is not None:
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
        myuser = User()
        myuser.userlogout(request)
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

    @api_view(['POST'])
    def updateUser(request):
        try:
            user1 = request.user
            if user1.role != 'UserAdmin':
                return Response({'message': 'You don\'t have permission to update account'}, status=403)

            user = User()
            username = request.data.get('username')
            email = request.data.get('email')
            password = request.data.get('password')
            # Retrieve the user with the specified username 
            myusr = user.userget(username)
            
            if email == "": email = None
            if password == "": password = None

            myusr.userupdate(email, password)
            return Response(status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    @api_view(['POST'])
    def deleteUser(request):
        try:
            user1 = request.user
            if user1.role != 'UserAdmin':
                return Response({'message': 'You don\'t have permission to update account'}, status=403)
            # Get the username from the request data
            user = User()
            username = request.data.get('username')
            # Retrieve the user with the specified username 
            myusr = user.userget(username)
            myusr.userdelete()
            return Response(status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        
    '''
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
    '''

class SearchUserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @api_view(['POST'])
    def searchUser(request):
         # Check if user has permission to search user
        if request.user.role != 'UserAdmin':
           raise PermissionDenied("You do not have permission to search user.")
        # Get prompt from request body
        keyword = request.data.get('keyword', '')
        if not keyword:
            return JsonResponse({'error': 'Please provide a keyword to search for'})
        
        result = User.usersearch(keyword)
        users = [u for u in result]
        data = [{'id': u.id, 'username': u.username, 'email': u.email, 'role': u.role} for u in users]
        return Response(data)
    
class UserProfile(APIView):
    Authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @api_view(['POST'])
    def createProfile(request):
        # Get the user data from the request
        username = request.data.get('username')
        name = request.data.get('name')
        date_of_birth = request.data.get('date_of_birth')

        user = User()
        profile = Profile()
        user_obj = user.userget(username)

        profile.profilecreate(user_obj, name, date_of_birth)

        # Return a response with the created profile data
        return Response(status=status.HTTP_200_OK)
    
    @api_view(['GET'])
    def viewProfile(request):
        # check if user has permission to view profiles
        if request.user.role != 'UserAdmin' and not request.user.is_superuser:
            raise PermissionDenied("You do not have permission to view profiles.")

        result = Profile.profileall()
        profiles = [p for p in result]
        data = [{'id': p.id, 'user': p.user.username, 'name': p.name, 'date_of_birth': p.date_of_birth} for p in profiles]
        return Response(data)
    
    @api_view(['POST'])
    def searchProfile(request):
        keyword = request.data.get('keyword', '')
        if not keyword:
            return JsonResponse({'error': 'Please provide a keyword to search for'})
        
        result = Profile.profilesearch(keyword)
        profiles = [p for p in result]
        data = [{'id': p.id, 'user': p.user.username, 'name': p.name, 'date_of_birth': p.date_of_birth} for p in profiles]
        return Response(data)
    
    @api_view(['POST'])
    def deleteProfile(request):
        try:
            user1 = request.user
            if user1.role != 'UserAdmin':
               return Response({'message': 'You don\'t have permission to update account'}, status=403)
            # Get the username from the request data
            profile = Profile()
            id = request.data.get('id')
            # Retrieve the user with the specified username 
            myprofile = profile.profileget(id)
            myprofile.profiledelete()
            return Response(status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response({'message': 'Profile not found.'}, status=status.HTTP_404_NOT_FOUND)
    
class Movies(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    @api_view(['POST'])
    def addMov(request):
        # Check if user is a cinemaManager
        if request.user.role != 'CinemaManager':
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        # Get the user data from the request
        movie_title = request.data.get('movie_title')
        genre = request.data.get('genre')
        duration = request.data.get('duration')
        release_date = request.data.get('release_date')
        cast = request.data.get('cast')
        director = request.data.get('director')
        movie_description = request.data.get('movie_description')
        posterIMG = request.data.get('posterIMG')
        featureIMG = request.data.get('featureIMG')

        movie = Movie()
        movie.moviecreate(movie_title, genre, duration, release_date, cast, director, movie_description, posterIMG, featureIMG)

        # Return a response with the created profile data
        return Response(status=status.HTTP_200_OK)
        
    @api_view(['POST'])
    def delMov(request):
        # Check if user is a cinemaManager
        if request.user.role != 'CinemaManager':
            return Response(status=status.HTTP_403_FORBIDDEN)

        movie = Movie()
        movie_title = request.data.get('movie_title')
        try:
            movie_obj = movie.movieget(movie_title)
        except Movie.DoesNotExist:
            # If the movie does not exist, return 404 error
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # Delete the movie from the database
        movie_obj.moviedelete()
        # Return a success response
        return Response(status=status.HTTP_200_OK)
    
    @api_view(['POST'])    
    def updateMov(request):
        
        # Check if user is a cinemaManager
        if request.user.role != 'CinemaManager':
            return Response(status=status.HTTP_403_FORBIDDEN)

        movie = Movie()
        movie_title = request.data.get('movie_title')
        genre = request.data.get('genre')
        duration = request.data.get('duration')
        release_date = request.data.get('release_date')
        cast = request.data.get('cast')
        director = request.data.get('director')
        movie_description = request.data.get('movie_description')
        posterIMG = request.data.get('posterIMG')
        featureIMG = request.data.get('featureIMG')

        if genre == "":
            genre = None
        if duration == "":
            duration = None
        if release_date == "":
            release_date = None
        if cast == "":
            cast = None
        if director == "":
            director = None
        if movie_description == "":
            movie_description = None
        if posterIMG == "":
            posterIMG = None
        if featureIMG == "":
            featureIMG = None

        try:
            movie_obj = movie.movieget(movie_title)
        except Movie.DoesNotExist:
            # If the movie does not exist, return 404 error
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # Delete the movie from the database
        movie_obj.movieupdate(genre, duration, release_date, cast, director, movie_description, posterIMG, featureIMG)
        # Return a success response
        return Response(status=status.HTTP_200_OK)
        
    @api_view(['POST'])
    def addCR(request):
        # Check if user is a cinemaManager.
        if request.user.role != 'CinemaManager':
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        # Get the user data from the request
        name = request.data.get('name')
        capacity = request.data.get('capacity')

        cr = CinemaRoom()
        cr.cinemaroomcreate(name, capacity)

        # Return a response with the created profile data
        return Response(status=status.HTTP_200_OK)


        
    @api_view(['POST'])
    def updateCR(request):
        # Check if user is a cinemaManager.
        if request.user.role != 'CinemaManager':
            return Response(status=status.HTTP_403_FORBIDDEN)

        # Get the movie object to update
        name = request.data.get('name')
        capacity = request.data.get('capacity')
        cinemaRoom = CinemaRoom()
        try:
            cr = cinemaRoom.cinemaroomget(name)
        except CinemaRoom.DoesNotExist:
            return Response({'message': 'Cinema Room does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        if capacity == "":
            capacity = None
        cr.cinemaroomupdate(capacity)
        return Response(status=status.HTTP_200_OK)
        
    @api_view(['POST'])
    def delCR(request):
         # Check if user is a cinemaManager.
        if request.user.role != 'CinemaManager':
           return Response(status=status.HTTP_403_FORBIDDEN)

        # Get the cinema room object to delete
        name = request.data.get('name')
        cinemaroom = CinemaRoom()
        try:
            cr = cinemaroom.cinemaroomsearch(name)
        except CinemaRoom.DoesNotExist:
            return Response({'message': 'Cinema Room does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        # Delete the cinema room
        cr.delete()
        return Response(status=status.HTTP_200_OK)
    


class MovieSessionC(APIView):
    Authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @api_view(['POST'])
    def addMS(request):
        # Check if user is a cinemaManager.
        if request.user.role != 'CinemaManager':
            return Response(status=status.HTTP_403_FORBIDDEN)

        movie = Movie()
        cinemaroom = CinemaRoom()
        moviesession = MovieSession()

        # Get movie, session date, cinema room and session time from request data
        movie_title = request.data['movie_title']
        session_date = request.data['session_date']
        cinema_room_name = request.data['cinema_room']
        session_time = request.data['session_time']

        # Retrieve movie and cinema room objects from the database
        try:
            mov = movie.movieget(movie_title)
            cr = cinemaroom.cinemaroomget(cinema_room_name)
        except (Movie.DoesNotExist, CinemaRoom.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Check if session time is valid
        valid_session_times = ['8:30', '11:30', '14:00', '16:30', '17:50', '18:40', '19:30', '20:40', '21:10']
        if session_time not in valid_session_times:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # Create new movie session
        moviesession.moviesessioncreate(mov, session_date, cr, session_time)

        return Response(status=status.HTTP_200_OK)
    
    @api_view(['GET'])
    def viewAllMS(request):
        # Check if user is a cinemaManager.
        if request.user.role != 'CinemaManager':
           return Response(status=status.HTTP_403_FORBIDDEN)

        # Retrieve all movie sessions from the database
        result = MovieSession.moviesessionall()
        sessions = [s for s in result]
        data = [{'id': s.id, 'movie': s.movie.movie_title, 'session_date': s.session_date, 'cinema_room': s.cinema_room.name} for s in sessions]
        return Response(data)
    
    @api_view(['POST'])
    #Search by movie session id
    def delMS(request):
        # Check if user is a cinemaManager.
        if request.user.role != 'CinemaManager':
            return Response(status=status.HTTP_403_FORBIDDEN)
        myid = request.data['id']  
        moviesession = MovieSession()   

        try:
            ms = moviesession.moviesessionget(myid)
            if not moviesession:
                raise MovieSession.DoesNotExist
        except MovieSession.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        ms.moviesessiondelete()
        return Response(status=status.HTTP_200_OK)
    
        

class allowAnyMovie(APIView):
    permission_classes = [AllowAny]

    @api_view(['POST'])
    def SearchMov(request):
        keyword = request.data.get('keyword', '')
        if not keyword:
            return JsonResponse({'error': 'Please provide a keyword to search for'})
        
        result = Movie.moviesearch(keyword)
        movies = [m for m in result]
        data = [{'movie_title': m.movie_title,
            'genre': m.genre,
            'duration': m.duration,
            'release_date': m.release_date,
            'cast': m.cast,
            'director': m.director,
            'movie_description': m.movie_description,
            'posterIMG': m.posterIMG,
            'featureIMG': m.featureIMG} for m in movies]
        return Response(data)
        
    @api_view(['GET'])   
    def viewAllCR(request):
        # Check if user is a cinemaManager.
        if request.user.role != 'CinemaManager':
            return Response(status=status.HTTP_403_FORBIDDEN)
        result = CinemaRoom.cinemaroomall()
        rooms = [r for r in result]
        data = [{'id': r.id, 'name': r.name, 'capacity': r.capacity} for r in rooms]
        return Response(data)

        
    @api_view(['GET'])
    def viewAllMovie(request):
        """
        Returns a list of all movie images
        """
        result = Movie.movieall()
        movies = [m for m in result]
        data = [{'movie_title': m.movie_title,
            'genre': m.genre,
            'duration': m.duration,
            'release_date': m.release_date,
            'cast': m.cast,
            'director': m.director,
            'movie_description': m.movie_description,
            'posterIMG': m.posterIMG,
            'featureIMG': m.featureIMG} for m in movies]
        return Response(data)
    
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
    
    @api_view(['POST'])
    def getMovieSession(request):
        try:
            movie_title = request.data['movie_title']
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            movie = Movie.objects.get(movie_title=movie_title)
            sessions = MovieSession.objects.filter(movie=movie)
        except (Movie.DoesNotExist, CinemaRoom.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)

        serialized_sessions = MovieSessionSerializer(sessions, many=True).data
        return Response(serialized_sessions, status=status.HTTP_200_OK)

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
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @api_view(['POST'])
    def addBook(request):
        # Check if user is authenticated.
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        # Create serializer with data from request body
        serializer = PurchaseTicketSerializer(data=request.data)

        # Validate serializer data
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #still testing
    #@api_view(['POST']) 
    @api_view(['GET'])
    def viewAllBook(request):
        # Check if user is authenticated.
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        #try:
            username = request.data['booking_owner']
        #except KeyError:
        #    return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            #bookings = PurchaseTicket.objects.filter(booking_owner=username)
            bookings = PurchaseTicket.objects.filter(booking_owner=request.user)
        except PurchaseTicket.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = PurchaseTicketSerializer(bookings, many=True)
        return Response(serializer.data)