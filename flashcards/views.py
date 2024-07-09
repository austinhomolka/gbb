# flashcards/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Flashcard
from .forms import FlashcardForm

@login_required
def flashcard_list(request):
    flashcards = Flashcard.objects.filter(user=request.user)
    return render(request, 'flashcards/flashcard_list.html', {'flashcards': flashcards})

@login_required
def flashcard_create(request):
    if request.method == 'POST':
        form = FlashcardForm(request.POST)
        if form.is_valid():
            flashcard = form.save(commit=False)
            flashcard.user = request.user
            flashcard.save()
            return redirect('flashcard_list')
    else:
        form = FlashcardForm()
    return render(request, 'flashcards/flashcard_form.html', {'form': form})

@login_required
def flashcard_edit(request, pk):
    flashcard = get_object_or_404(Flashcard, pk=pk, user=request.user)
    if request.method == 'POST':
        form = FlashcardForm(request.POST, instance=flashcard)
        if form.is_valid():
            form.save()
            return redirect('flashcard_list')
    else:
        form = FlashcardForm(instance=flashcard)
    return render(request, 'flashcards/flashcard_form.html', {'form': form})

@login_required
def flashcard_delete(request, pk):
    flashcard = get_object_or_404(Flashcard, pk=pk, user=request.user)
    if request.method == 'POST':
        flashcard.delete()
        return redirect('flashcard_list')
    return render(request, 'flashcards/flashcard_confirm_delete.html', {'flashcard': flashcard})

@login_required
def shuffle(request):
    flashcards = list(Flashcard.objects.filter(user=request.user).order_by('?'))
    return render(request, 'flashcards/shuffle.html', {'flashcards': flashcards})

@login_required
def get_next_flashcard(request):
    flashcards = list(Flashcard.objects.filter(user=request.user).order_by('?'))
    if flashcards:
        flashcard = flashcards[0]
        return JsonResponse({
            'id': flashcard.id,
            'front_text': flashcard.front_text,
            'back_text': flashcard.back_text,
            'color': flashcard.color,
        })
    return JsonResponse({'error': 'No flashcards available'}, status=404)