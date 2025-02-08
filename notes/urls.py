from django.urls import path
from .views import create_note, get_notes, get_note_by_id, update_note, delete_note

urlpatterns = [
    path("index/notes/", get_notes, name="index"),
    path("show/notes/<int:note_id>/", get_note_by_id, name="show"),
    path("store/notes/", create_note, name="store"),
    path("update/notes/<int:note_id>/", update_note, name="update"),
    path("destroy/notes/<int:note_id>/", delete_note, name="destroy"),
]
