from django.urls import path
from core.views import upload_images

urlpatterns = [
    # other URL patterns
    path('movies/<int:movie_id>/upload_images/', upload_images, name='upload_images'),
]