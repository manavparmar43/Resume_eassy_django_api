from django.shortcuts import render, get_object_or_404
from django.contrib import auth
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from account.serializers import UserSerializer
from django.template.loader import get_template
from django.core.mail import EmailMessage

from .models import NonBuiltInUserToken, User
from django.conf import settings
from django.core.mail import send_mail


# Create your views here.

# class RegisterApi()


class RegisterApi(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save(password=make_password(request.data.get("password")))
            token = NonBuiltInUserToken.objects.create(user_id=user.id)
            return Response(
                {"Token": str(token), "is_superuser": user.is_superuser},
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors)


class LoginApi(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get("username", None)
        password = request.data.get("password", None)

        try:
            user = User.objects.filter(username=username).first()
            if user:
                if username and password:
                    user = auth.authenticate(username=username, password=password)
                    if user:
                        token = NonBuiltInUserToken.objects.create(user_id=user.id)
                        return Response(
                            {"Token": str(token), "is_superuser": user.is_superuser},
                            200,
                        )
                    else:
                        return Response(
                            "Invalid Password", status=status.HTTP_401_UNAUTHORIZED
                        )
                else:
                    return Response("Please enter the required fields", 203)
            else:
                return Response(
                    "Username not found", status=status.HTTP_401_UNAUTHORIZED
                )
        except:
            return Response("Invalid Password", status=status.HTTP_401_UNAUTHORIZED)


class ForgotPasswordApi(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        site = settings.FRONT_URL

        user = User.objects.filter(email=email).first()
        if user:
            try:
                url = site + "reset-password/" + str(user.id)
                message = get_template("reset-password.html").render(
                    {"username": user.username, "link": url, "name": user.name}
                )
                mail = EmailMessage(
                    subject="Your viuw reset-password link",
                    body=message,
                    from_email=settings.EMAIL_HOST_USER,
                    to=[
                        email,
                    ],
                )
                mail.content_subtype = "html"
                mail.send(fail_silently=False)

                return Response("Email has been sent on your registered Email ID", 200)
            except:
                return Response("Something went wrong", 400)
        return Response("No user with the given Email", 203)


class ResetPasswordApi(APIView):
    def post(self, request, id=None, *args, **kwargs):
        password = request.data.get("password")
        confirm_password = request.data.get("confirm_password")
        user = User.objects.get(id=id)
        if password == confirm_password:
            user.set_password(password)
            user.save()
            return Response("Password Changed Succesfully", 201)

        return Response("Password and confirm-password does not match", 203)
