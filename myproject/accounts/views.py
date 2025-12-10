from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import RegistrationSerializer, LoginSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .tokens import CustomTokenObtainPairSerializer

class RegistrationView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = (AllowAny,)

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
