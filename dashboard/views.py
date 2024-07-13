from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from flashcards.models import Deck
import logging
from django.http import HttpResponseServerError

logger = logging.getLogger(__name__)

# Home view redirects to dashboard if the user is authenticated, else to login
def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')

# Dashboard view shows the user's decks
@login_required
def dashboard(request):
    try:
        decks = Deck.objects.filter(user=request.user)
        return render(request, 'dashboard.html', {'decks': decks})
    except Exception as e:
        logger.error(f"Error in dashboard view: {str(e)}")
        return HttpResponseServerError("An error occurred. Please try again later.")

# Sign-up view handles user registration
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.email = form.cleaned_data.get('username')
            user.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

# Login view handles user authentication
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Logout view logs out the user and redirects to login
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
