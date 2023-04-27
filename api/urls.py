from django.urls import include, path
from .views import AccountController, LoginView, LogoutView, GetUserView, UpdateUser


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
    path('changeEmail/', UpdateUser.changeEmail, name='changeEmail')
]