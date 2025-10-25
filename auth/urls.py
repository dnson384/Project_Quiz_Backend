from django.urls import path
from .views import RegisterWithEmailView, LoginWithEmailView

urlpatterns = [
    path("register", RegisterWithEmailView.as_view(), name="register-email"),
    path("login", LoginWithEmailView.as_view(), name="login-email"),
]
