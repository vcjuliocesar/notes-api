from django.db import models
from django.contrib.auth.models import User

# Create your models here.

CATEGORY = (
    ("BUSINESS", "Business"),
    ("PERSONAL", "Personal"),
    ("IMPORTANT", "Important"),
)


class Note(models.Model):
    title = models.CharField(unique=True,max_length=100)
    body = models.TextField()
    category = models.CharField(max_length=20,choices=CATEGORY, default="PERSONAL")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
