from django.urls import include, path
from .views import AccountController
urlpatterns = [
    # other URL patterns here
    path('', AccountController.getUserAccount),
    path('add/', AccountController.addUserAccount)
]