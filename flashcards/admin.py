from django.contrib import admin
from .models import Deck, Flashcard

class FlashcardInline(admin.TabularInline):
    model = Flashcard
    extra = 1

@admin.register(Deck)
class DeckAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at', 'flashcard_count')
    list_filter = ('user', 'created_at')
    search_fields = ('name', 'user__username')
    inlines = [FlashcardInline]

    def flashcard_count(self, obj):
        return obj.flashcards.count()
    flashcard_count.short_description = 'Number of Flashcards'

@admin.register(Flashcard)
class FlashcardAdmin(admin.ModelAdmin):
    list_display = ('front_text', 'back_text', 'deck', 'user', 'created_at')
    list_filter = ('deck', 'user', 'created_at')
    search_fields = ('front_text', 'back_text', 'deck__name', 'user__username')