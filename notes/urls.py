from django.urls import path
from .views import create_note

urlpatterns = [
    path('create/',create_note)
]