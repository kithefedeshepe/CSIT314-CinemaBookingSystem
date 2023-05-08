from django.urls import include, path
from .views import AccountController, LoginView, LogoutView, GetUserView, UpdateUser, SearchUserView, UserProfile, movieIMG, Movies, allowAnyMovie, Fnbs


urlpatterns = [
    # other URL patterns here
    path('', AccountController.getUserAccount),
    path('add/', AccountController.RegisterAccount, name='add'),
    path('login/', LoginView.login, name='login'),
    path('logout/', LogoutView.logout, name='logout'),
    path('getUser/', GetUserView.getUser, name="getUser"),
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
    path('SearchMovie/', allowAnyMovie.SearchMov, name='SearchMovie'),
    path('delImg/', movieIMG.delImg, name='delImg'),
    path('updateMov/', Movies.updateMov, name='updateMov'),
    path('view/', allowAnyMovie.viewAllMovie, name='viewMov'),
    path('addCR/', Movies.addCR, name='addCR'),
    path('viewAllCR/', Movies.viewAllCR, name='viewAllCR'),
    path('updateCR/', Movies.updateCR, name='updateCR'),
    path('delCR/', Movies.delCR, name='delCR'),
    path('addFnb/', Fnbs.addFnb, name='addFnb'),
    path('viewAllFnb/', Fnbs.viewAllFnb, name='viewAllFnb'),
    path('updateFnB/', Fnbs.updateFnB, name='updateFnB'),
    path('delFnB/', Fnbs.delFnB, name='delFnB')
]