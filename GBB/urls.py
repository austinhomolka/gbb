from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from dashboard import views as dashboard_views
from flashcards import views as flashcard_views

def trigger_error(request):
    division_by_zero = 1 / 0

urlpatterns = [
    path('sentry-debug/', trigger_error),
    path('admin/', admin.site.urls),
    path('', dashboard_views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('sign-up/', dashboard_views.signup, name='signup'),
    path('logout/', dashboard_views.logout_view, name='logout'),
    path('dashboard/', dashboard_views.dashboard, name='dashboard'),
    
    # Deck URLs
    path('decks/', flashcard_views.deck_list, name='deck_list'),
    path('decks/create/', flashcard_views.create_deck, name='create_deck'),
    path('decks/<int:deck_id>/', flashcard_views.deck_detail, name='deck_detail'),
    path('decks/<int:deck_id>/create_flashcard/', flashcard_views.create_flashcard, name='create_flashcard'),
    path('decks/<int:deck_id>/shuffle/', flashcard_views.shuffle_deck, name='shuffle_deck'),
    
    # Flashcard URLs
    path('flashcards/<int:flashcard_id>/edit/', flashcard_views.edit_flashcard, name='edit_flashcard'),
    path('flashcards/<int:flashcard_id>/delete/', flashcard_views.delete_flashcard, name='delete_flashcard'),
    
    # Shuffle and AJAX
    path('shuffle_all/', flashcard_views.shuffle_all, name='shuffle_all'),
    path('get_next_flashcard/', flashcard_views.get_next_flashcard, name='get_next_flashcard'),
]