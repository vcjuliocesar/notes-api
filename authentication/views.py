from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth.models import User
from authentication import serializer
from .serializer import UserSerializer

# Create your views here.


@api_view(["POST"])
def register(request):

    serializer = UserSerializer(data=request.data)

    if not serializer.is_valid():

        return Response(
            {"error", serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )

    serializer.save()

    user = User.objects.get(username=request.data["username"])
    user.set_password(serializer.data["password"])
    user.save()

    token = Token.objects.create(user=user)

    return Response(
        {"token": token.key, "user": serializer.data}, status=status.HTTP_201_CREATED
    )


@api_view(["POST"])
def login(request):

    username = request.data["username"].strip()

    password = request.data["password"].strip()

    user = get_object_or_404(User, username=username)

    if not user.check_password(password):

        return Response(
            {"error", "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )

    token, created = Token.objects.get_or_create(user=user)

    serializer = UserSerializer(instace=user)

    return Response(
        {"token": token.key, "user": serializer.data}, status=status.HTTP_200_OK
    )
