from django.shortcuts import render, get_objet_or_404, redirect
from django.http import HttpResponse
from .models import CustomUserManager, User, CinemaRoom, Movie Session, Profile, Movie
from django.view.generic import CreateView
from .forms import Profile