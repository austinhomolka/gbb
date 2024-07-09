# flashcards/models.py

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Flashcard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    front_text = models.TextField()
    back_text = models.TextField()
    # icon = models.ImageField(upload_to='flashcard_icons/', null=True, blank=True)
    color = models.CharField(max_length=7, default='#FFFFFF')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Flashcard {self.id} - {self.front_text[:20]}"