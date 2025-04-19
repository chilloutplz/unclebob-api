from django.urls import path
from .views import RegisterView, LoginView
from rest_framework_simplejwt.views import(
    TokenObtainPairView,
    # TokenVerifyView,
    # TokenBlacklistView,
    TokenRefreshView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
