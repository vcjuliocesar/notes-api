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
from .models import Note


# Create your views here.
@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_note(request):
    user = request.user
    note_serializer = NoteSerializer(data=request.data)

    if not note_serializer.is_valid():
        return Response(note_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    note = note_serializer.save(user=user)

    return Response(NoteSerializer(note).data, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_notes(request):
    user = request.user
    notes = Note.objects.filter(user=user)
    serializer = NoteSerializer(notes, many=True)
    return Response({"data": serializer.data}, status=status.HTTP_200_OK)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_note_by_id(request, note_id):
    user = request.user
    try:
        notes = Note.objects.filter(id=note_id, user=user)

        if not notes:
            return Response(
                {"error": "The note does not exist"}, status=status.HTTP_400_BAD_REQUEST
            )

        serializer = NoteSerializer(notes, many=True)

        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
    except Exception as error:
        raise error


@api_view(["PUT"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_note(request, note_id):
    user = request.user
    try:
        note = Note.objects.get(id=note_id, user=user)

        if not note:
            return Response(
                {"error": "The note does not exist"}, status=status.HTTP_400_BAD_REQUEST
            )

        serializer = NoteSerializer(instance=note, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    except Note.DoesNotExist:
        return Response(
            {"error": "The note does not exist"}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_note(request, note_id):
    user = request.user
    try:
        note = Note.objects.get(id=note_id, user=user)

        if not note:
            return Response(
                {"error": "The note does not exist"}, status=status.HTTP_400_BAD_REQUEST
            )
        note.delete()
        return Response(
            {"message": "Note deleted successfully"}, status=status.HTTP_204_NO_CONTENT
        )

    except Note.DoesNotExist:
        return Response(
            {"error": "The note does not exist"}, status=status.HTTP_400_BAD_REQUEST
        )
