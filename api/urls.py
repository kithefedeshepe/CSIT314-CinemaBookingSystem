from django.urls import include, path
from .views import AccountController, LoginView, LogoutView


urlpatterns = [
    # other URL patterns here
    path('', AccountController.getUserAccount),
    path('add/', AccountController.RegisterAccount),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view())
]