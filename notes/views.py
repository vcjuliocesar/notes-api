from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from authentication.serializer import UserSerializer
from .serializer import NoteSerializer


# Create your views here.
@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_note(request):
    user = request.user
    note_serializer = NoteSerializer(data=request.data)
    
    if not note_serializer.is_valid():
        return Response(note_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    note = note_serializer.save(user = user)
    
    return Response(NoteSerializer(note).data, status=status.HTTP_201_CREATED)
