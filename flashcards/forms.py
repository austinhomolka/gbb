# flashcards/forms.py

from django import forms
from .models import Flashcard

class FlashcardForm(forms.ModelForm):
    class Meta:
        model = Flashcard
        fields = ['front_text', 'back_text', 'color']
        widgets = {
            'color': forms.TextInput(attrs={'type': 'color'}),
        }