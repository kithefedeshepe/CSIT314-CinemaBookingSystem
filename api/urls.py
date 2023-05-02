from django.urls import include, path
from .views import AccountController, LoginView, LogoutView, GetUserView, UpdateUser, SearchUserView, UserProfile, movieIMG, Movies, SearchMovie


urlpatterns = [
    # other URL patterns here
    path('', AccountController.getUserAccount),
    path('add/', AccountController.RegisterAccount, name='add'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('getUser/', GetUserView.as_view()),
    path('suspendUser/', UpdateUser.suspendUser, name='suspendUser'),
    path('reactivateUser/', UpdateUser.reactivateUser, name='reactivateUser'),
    path('changePW/', UpdateUser.changePassword, name='changePassword'),
    path('changeEmail/', UpdateUser.changeEmail, name='changeEmail'),
    path('searchUser/', SearchUserView.searchUser, name='searchUser'),
    path('createProfile/', UserProfile.createProfile, name='createProfile'),
    path('viewProfile/', UserProfile.viewProfile, name='viewProfile'),
    path('getProfile/', UserProfile.getProfile, name='getProfile'),
    path('movieIMG/', movieIMG.viewMovieImage, name='movieIMG'),
    path('getMovieImage/', movieIMG.getMovieImage, name='getMovieImage'),
    path('addImg/', movieIMG.addMovieImg, name='addImg'),
    path('addMov/', Movies.addMov, name='addMov'),
    path('delMov/', Movies.delMov, name='delMov'),
    path('SearchMovie/', SearchMovie.SearchMov, name='SearchMovie')
]