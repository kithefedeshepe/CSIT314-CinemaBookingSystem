from django.urls import include, path
from .controllers import AccountController, LoginView, LogoutView, GetUserView, UpdateUser, SearchUserView, UserProfile, Movies, allowAnyMovie, Fnbs, Purchase, MovieSessionC


urlpatterns = [
    # Account
    path('', AccountController.getUserAccount),
    path('add/', AccountController.RegisterAccount, name='add'),

    # Log in/out
    path('login/', LoginView.login, name='login'),
    path('logout/', LogoutView.logout, name='logout'),
    path('getUser/', GetUserView.getUser, name="getUser"),

    # Account management
    #path('suspendUser/', UpdateUser.suspendUser, name='suspendUser'),
    #path('reactivateUser/', UpdateUser.reactivateUser, name='reactivateUser'),
    #path('changePW/', UpdateUser.changePassword, name='changePassword'),
    #path('changeEmail/', UpdateUser.changeEmail, name='changeEmail'),
    path('deleteUser/', UpdateUser.deleteUser, name='deleteUser'),
    path('updateUser/', UpdateUser.updateUser, name='updateUser'),
    path('searchUser/', SearchUserView.searchUser, name='searchUser'),

    #Profile management
    path('createProfile/', UserProfile.createProfile, name='createProfile'),
    path('viewProfile/', UserProfile.viewProfile, name='viewProfile'),
    path('searchProfile/', UserProfile.searchProfile, name='searchProfile'),
    path('deleteProfile/', UserProfile.deleteProfile, name='deleteProfile'),

    # Movie management
    path('addMov/', Movies.addMov, name='addMov'),
    path('delMov/', Movies.delMov, name='delMov'),
    path('searchMovie/', allowAnyMovie.SearchMov, name='SearchMovie'),
    path('updateMovie/', Movies.updateMov, name='updateMov'),
    path('view/', allowAnyMovie.viewAllMovie, name='viewMov'),

    # Cinema room management
    path('addCR/', Movies.addCR, name='addCR'),
    path('viewAllCR/', Movies.viewAllCR, name='viewAllCR'),
    path('updateCR/', Movies.updateCR, name='updateCR'),
    path('delCR/', Movies.delCR, name='delCR'),

    # Movie session management
    path('addMS/', MovieSessionC.addMS, name='addMS'),
    path('viewAllMS/', MovieSessionC.viewAllMS, name='viewAllMS'),
    path('delMS/', MovieSessionC.delMS, name='delMS'),
    path('getMovieSession/', allowAnyMovie.getMovieSession, name='getMovieSession'),

    # Fnb management
    path('addFnb/', Fnbs.addFnb, name='addFnb'),
    path('viewAllFnb/', Fnbs.viewAllFnb, name='viewAllFnb'),
    path('updateFnB/', Fnbs.updateFnB, name='updateFnb'),
    path('delFnB/', Fnbs.delFnB, name='delFnb'),

    # Purchase booking                                                                                      
    path('addBook/', Purchase.addBook, name='addBook'),
    path('viewAllBook/', Purchase.viewAllBook, name='viewAllBook'),

    #helper function
    path('viewUpcoming/', allowAnyMovie.getUpComing),
    path('viewNowShowing/', allowAnyMovie.getNowShowing)
]