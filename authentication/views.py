import re
from os import error
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth.models import User
from authentication import serializer
from .serializer import UserSerializer

# Create your views here.


def validate_password(password):
    pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@#$%^&*()-+=])[A-Za-z\d@#$%^&*()-+=]{8,}$"
    return bool(re.match(pattern, password))


@api_view(["POST"])
def register(request):

    try:
        if not validate_password(request.data["password"]):
            return Response(
                {
                    "error": "Invalid password",
                    "message": "The password must meet the following requirements:\n"
                    "- At least 8 characters in length\n"
                    "- At least one uppercase letter\n"
                    "- At least one lowercase letter\n"
                    "- At least one number\n"
                    "- At least one special character (@, #, $, %, &, *, etc.)",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = UserSerializer(data=request.data)

        if not serializer.is_valid():

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
       
        serializer.save()
        user = User.objects.get(username=request.data["username"])
        user.set_password(request.data["password"])
        user.save()

        token = Token.objects.create(user=user)

        return Response(
            {"token": token.key, "user": serializer.data},
            status=status.HTTP_201_CREATED,
        )
    except Exception as error:
        raise error


@api_view(["POST"])
def login(request):

    try:

        username = request.data["username"].strip()

        password = request.data["password"].strip()

        if username is None or not username:
            return Response(
                {"error", "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )

        if password is None or not password:
            return Response(
                {"error", "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )

        user = get_object_or_404(User, username=username)

        if not user.check_password(password):

            return Response(
                {"error", "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )

        token, created = Token.objects.get_or_create(user=user)

        serializer = UserSerializer(instance=user)

        return Response(
            {"token": token.key, "user": serializer.data}, status=status.HTTP_200_OK
        )
    except Exception as error:

        raise error
