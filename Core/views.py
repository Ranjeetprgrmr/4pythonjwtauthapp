from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

@api_view(['GET'])
def Home(request):
    return Response('Hello, world!')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def MyProtectedRoute(request):
    return Response("You have been granted access to my protected route")


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetUserInfo(request):
    user = request.user
    user_serializer = UserSerializer(user)
    
    return Response(user_serializer.data)




class MyTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        print("Token Response (Before Adding User):", response.data)  # Check tokens exist
        
        username = request.data.get('username')  # Use `request.data` for JSON payloads
        if username:
            user = User.objects.get(username=username)
            print("User Object:", user)  # Confirm user exists
            
            user_serializer = UserSerializer(user)
            print("Serialized User Data:", user_serializer.data)  # Verify serialization
            
            response.data['user'] = user_serializer.data
        return response