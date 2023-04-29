from django.urls import include, path
from .views import AccountController, LoginView, LogoutView, GetUserView, UpdateUser, SearchUserView, UserProfile, movieIMG, addImg


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
    path('movieIMG/', movieIMG.as_view(), name='movieIMG'),
    path('addImg/', addImg.as_view(), name='addImg')
]