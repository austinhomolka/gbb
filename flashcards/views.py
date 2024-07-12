from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Flashcard, Deck
from .forms import FlashcardForm, DeckForm
import random

@login_required
def deck_list(request):
    decks = Deck.objects.filter(user=request.user)
    return render(request, 'flashcards/deck_list.html', {'decks': decks})

@login_required
def deck_detail(request, deck_id):
    deck = get_object_or_404(Deck, id=deck_id, user=request.user)
    flashcards = deck.flashcards.all()
    return render(request, 'flashcards/deck_detail.html', {'deck': deck, 'flashcards': flashcards})

@login_required
def create_deck(request):
    if request.method == 'POST':
        form = DeckForm(request.POST)
        if form.is_valid():
            deck = form.save(commit=False)
            deck.user = request.user
            deck.save()
            return redirect('deck_list')
    else:
        form = DeckForm()
    return render(request, 'flashcards/deck_form.html', {'form': form})

@login_required
def create_flashcard(request, deck_id):
    deck = get_object_or_404(Deck, id=deck_id, user=request.user)
    if request.method == 'POST':
        form = FlashcardForm(request.POST)
        if form.is_valid():
            flashcard = form.save(commit=False)
            flashcard.user = request.user
            flashcard.deck = deck
            flashcard.save()
            return redirect('deck_detail', deck_id=deck.id)
    else:
        form = FlashcardForm()
    return render(request, 'flashcards/flashcard_form.html', {'form': form, 'deck': deck})

@login_required
def edit_flashcard(request, flashcard_id):
    flashcard = get_object_or_404(Flashcard, id=flashcard_id, user=request.user)
    if request.method == 'POST':
        form = FlashcardForm(request.POST, instance=flashcard)
        if form.is_valid():
            form.save()
            return redirect('deck_detail', deck_id=flashcard.deck.id)
    else:
        form = FlashcardForm(instance=flashcard)
    return render(request, 'flashcards/flashcard_form.html', {'form': form, 'flashcard': flashcard})

@login_required
def delete_flashcard(request, flashcard_id):
    flashcard = get_object_or_404(Flashcard, id=flashcard_id, user=request.user)
    deck_id = flashcard.deck.id
    if request.method == 'POST':
        flashcard.delete()
        return redirect('deck_detail', deck_id=deck_id)
    return render(request, 'flashcards/flashcard_confirm_delete.html', {'flashcard': flashcard})

@login_required
def shuffle_deck(request, deck_id):
    deck = get_object_or_404(Deck, id=deck_id, user=request.user)
    flashcards = list(deck.flashcards.all().order_by('?'))
    return render(request, 'flashcards/shuffle.html', {'flashcards': flashcards, 'deck': deck})

@login_required
def shuffle_all(request):
    flashcards = list(Flashcard.objects.filter(user=request.user).order_by('?'))
    return render(request, 'flashcards/shuffle.html', {'flashcards': flashcards, 'all_decks': True})

@login_required
def get_next_flashcard(request):
    deck_id = request.GET.get('deck_id')
    
    if deck_id:
        try:
            deck = Deck.objects.get(id=deck_id, user=request.user)
            flashcards = deck.flashcards.all()
        except Deck.DoesNotExist:
            return JsonResponse({'error': 'Deck not found'}, status=404)
    else:
        flashcards = Flashcard.objects.filter(user=request.user)
    
    if not flashcards:
        return JsonResponse({'error': 'No flashcards available'}, status=404)
    
    flashcard = random.choice(flashcards)
    return JsonResponse({
        'id': flashcard.id,
        'front_text': flashcard.front_text,
        'back_text': flashcard.back_text,
        'color': flashcard.color,
    })