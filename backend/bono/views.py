# bono/views.py
from rest_framework import generics, response
from .models import Bonos
from .serializers import BonoSerializer, CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate

class BonoListCreateView(generics.ListCreateAPIView):
    queryset = Bonos.objects.all()
    serializer_class = BonoSerializer

class BonoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bonos.objects.all()
    serializer_class = BonoSerializer

""" class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
 """

@api_view(['POST'])
def user_login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    # Check if both username and password are provided
    if not username or not password:
        return Response({"detail": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

    # Authenticate the user
    user = authenticate(request, username=username, password=password)

    # Check if authentication is successful
    if user is not None:
        # Additional checks for user status
        if not user.is_active or user.is_deleted:
            return Response({"detail": "User account is inactive or has been deleted."}, status=status.HTTP_403_FORBIDDEN)

        # Generate tokens using the custom serializer
        serializer = CustomTokenObtainPairSerializer(data=request.data)
        
        if serializer.is_valid():
            # Return both access and refresh tokens in response
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        # Incorrect username or password
        return Response({"detail": "Invalid username or password."}, status=status.HTTP_401_UNAUTHORIZED)
