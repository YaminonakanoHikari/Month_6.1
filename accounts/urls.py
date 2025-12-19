from django.urls import path
from .views import RegistrationView, LoginView
from .views import CustomTokenObtainPairView
from . import views
from .views import SendConfirmationCodeView, VerifyConfirmationCodeView

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('google/login/', views.google_login, name='google-login'),
    path('google/callback/', views.google_callback, name='google-callback'),
    path('send-code/', SendConfirmationCodeView.as_view(), name='send-code'),
    path('verify-code/', VerifyConfirmationCodeView.as_view(), name='verify-code'),
]