# accounts/views.py
from django.shortcuts import redirect
from django.conf import settings
from django.utils import timezone
from rest_framework.response import Response
import requests
from .models import CustomUser
from rest_framework import generics, status
from .serializers import RegistrationSerializer, LoginSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .tokens import CustomTokenObtainPairSerializer

# ===== Registration/Login/Token views =====
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

# ===== Google OAuth =====
def google_login(request):
    redirect_uri = "http://127.0.0.1:8000/accounts/google/callback/"
    client_id = settings.GOOGLE_CLIENT_ID
    google_url = (
        "https://accounts.google.com/o/oauth2/v2/auth"
        f"?client_id={client_id}"
        f"&redirect_uri={redirect_uri}"
        "&response_type=code"
        "&scope=openid%20email%20profile"
    )
    return redirect(google_url)

def google_callback(request):
    code = request.GET.get("code")
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": "http://127.0.0.1:8000/accounts/google/callback/",
        "grant_type": "authorization_code",
    }
    token_data = requests.post(token_url, data=data).json()
    access_token = token_data.get("access_token")

    userinfo_url = "https://www.googleapis.com/oauth2/v2/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}
    google_user = requests.get(userinfo_url, headers=headers).json()

    email = google_user["email"]
    user, created = CustomUser.objects.get_or_create(email=email)
    user.first_name = google_user.get("given_name", "")
    user.last_name = google_user.get("family_name", "")
    user.registration_source = "google"
    user.is_active = True
    user.last_login = timezone.now()
    user.save()

    return Response({
        "message": "Google login successful",
        "email": user.email
    })
