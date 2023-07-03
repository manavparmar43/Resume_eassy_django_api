from django.urls import path
from .views import *

urlpatterns = [
    path("login", LoginApi.as_view(), name="login"),
    path("register", RegisterApi.as_view(), name="register"),
    path("forgot-password", ForgotPasswordApi.as_view(), name="forgot"),
    path("reset-password/<id>", ResetPasswordApi.as_view(), name="reset-password"),
]
