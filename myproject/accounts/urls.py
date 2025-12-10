from django.urls import path
from .views import RegistrationView, LoginView
from .views import CustomTokenObtainPairView

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
]
