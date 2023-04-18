from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
# Create your views here.

@api_view(['get'])
def getData(request):
    person =  {'name': 'lmaoez'}
    return Response(person)
