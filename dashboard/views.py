# dashboard/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from flashcards.models import Flashcard, Deck
import logging
from django.http import HttpResponseServerError

# Define the custom sign-up form
class SignUpForm(UserCreationForm):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('email', 'name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['email'].label = "Email"

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.username = self.cleaned_data["email"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

# Home view redirects to dashboard if the user is authenticated, else to login
def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')

# Set up logging
logger = logging.getLogger(__name__)

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
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.first_name = form.cleaned_data.get('name').split()[0]
            user.last_name = ' '.join(form.cleaned_data.get('name').split()[1:])
            user.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

# Logout view logs out the user and redirects to login
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
