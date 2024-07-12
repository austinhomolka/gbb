from django import forms
from .models import Flashcard, Deck

class DeckForm(forms.ModelForm):
    class Meta:
        model = Deck
        fields = ['name']

class FlashcardForm(forms.ModelForm):
    class Meta:
        model = Flashcard
        fields = ['front_text', 'back_text', 'color']