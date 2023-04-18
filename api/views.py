from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from core.models import User
from .serializers import UserSerializer
# Create your views here.

@api_view(['GET'])
def getUserAccount(request):
    user_account = User.objects.all()
    serializer = UserSerializer(user_account, many = True)
    return Response(serializer.data)

@api_view(['POST'])
def addUserAccount(request):
    serializer = UserSerializer(data=request.data)
    if serializer.isvalid(raise_execption=True):
        serializer.save()
        return Response()
    return Response({"invalid":"bad entry"}, status=400)