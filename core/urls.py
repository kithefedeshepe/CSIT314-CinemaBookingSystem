from django.urls import path, include
from .views import index

urls_pattern = [
    path('', index),
]