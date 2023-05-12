from django.urls import include, path
from .controllers import AccountController, UpdateProfile, SearchFnbs, SearchMovieSession, SearchCinemaRoom, LoginView, LogoutView, GetUserView, UpdateUser, SearchUserView, DeleteUser, CreateProfile, ViewProfile, SearchProfile, DeleteProfile, AddMovie, DeleteMovie, SearchMovie, UpdateMovie, ViewAllMovie, AddCinemaRoom, ViewAllCinemaRoom, DeleteCinemaRoom, UpdateCinemaRoom, DeleteMovieSession, AddMovieSession, ViewAllMovieSession, HelperFunction, AddFnbs, ViewAllFnbs, UpdateFnbs, DeleteFnbs, AddBooking, ViewAllBooking, UpdateMovieSession, CreateFnBBooking, ViewFnBBooking, DeleteFnBBooking

urlpatterns = [
    # Account
    path('', AccountController.getUserAccount),
    path('add/', AccountController.RegisterAccount, name='add'),

    # Log in/out
    path('login/', LoginView.login, name='login'),
    path('logout/', LogoutView.logout, name='logout'),
    path('getUser/', GetUserView.getUser, name="getUser"),

    # User management
    path('deleteUser/', DeleteUser.deleteUser, name='deleteUser'),
    path('updateUser/', UpdateUser.updateUser, name='updateUser'),
    path('searchUser/', SearchUserView.searchUser, name='searchUser'),

    #Profile management
    path('createProfile/', CreateProfile.createProfile, name='createProfile'),
    path('viewProfile/', ViewProfile.viewProfile, name='viewProfile'),
    path('searchProfile/', SearchProfile.searchProfile, name='searchProfile'),
    path('deleteProfile/', DeleteProfile.deleteProfile, name='deleteProfile'),
    path('updateProfile/', UpdateProfile.updateProfile, name='updateProfile'),
    # Movie management
    path('addMov/', AddMovie.addMov, name='addMov'),
    path('delMov/', DeleteMovie.delMov, name='delMov'),
    path('searchMovie/', SearchMovie.SearchMov, name='SearchMovie'),
    path('updateMovie/', UpdateMovie.updateMov, name='updateMov'),
    path('viewMov/', ViewAllMovie.viewAllMovie, name='viewMov'),

    # Cinema room management
    path('addCR/', AddCinemaRoom.addCR, name='addCR'),
    path('viewAllCR/', ViewAllCinemaRoom.viewAllCR, name='viewAllCR'),
    path('updateCR/', UpdateCinemaRoom.updateCR, name='updateCR'),
    path('searchCR/', SearchCinemaRoom.searchCR, name='searchCR'),
    path('delCR/', DeleteCinemaRoom.delCR, name='delCR'),

    # Movie session management
    path('addMS/', AddMovieSession.addMS, name='addMS'),
    path('viewAllMS/', ViewAllMovieSession.viewAllMS, name='viewAllMS'),
    path('delMS/', DeleteMovieSession.delMS, name='delMS'),
    path('getMovieSession/', HelperFunction.getMovieSession, name='getMovieSession'),
    path('updateMovieSession', UpdateMovieSession.updateMS, name = 'updateMs'),
    path('searchMovieSession', SearchMovieSession.searchMS, name = 'searchMs'),

    # Fnb management
    path('addFnb/', AddFnbs.addFnb, name='addFnb'),
    path('viewAllFnb/', ViewAllFnbs.viewAllFnb, name='viewAllFnb'),
    path('updateFnB/', UpdateFnbs.updateFnB, name='updateFnb'),
    path('delFnB/', DeleteFnbs.delFnB, name='delFnb'),
    path('searchFnB/', SearchFnbs.searchFnB, name='searchFnb'),

    # FnBBooking Management
    path('purchaseFnB/', CreateFnBBooking.purchaseFnB, name='purchaseFnB'),
    path('viewFnBBooking/', ViewFnBBooking.viewAllFnBBooking, name='viewFnBBooking'),
    path('delFnBBooking/', DeleteFnBBooking.delFnBBooking, name='delFnBBooking'),

    # Purchase booking                                                                                      
    path('addBook/', AddBooking.addBook, name='addBook'),
    path('viewAllBook/', ViewAllBooking.viewAllBook, name='viewAllBook'),

    #helper function
    path('viewUpcoming/', HelperFunction.getUpComing),
    path('viewNowShowing/', HelperFunction.getNowShowing)
]