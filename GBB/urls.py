# GBB/urls.py

from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from dashboard import views as dashboard_views
from flashcards import views as flashcard_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard_views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('sign-up/', dashboard_views.signup, name='signup'),
    path('logout/', dashboard_views.logout_view, name='logout'),
    path('dashboard/', dashboard_views.dashboard, name='dashboard'),
    path('flashcards/', flashcard_views.flashcard_list, name='flashcard_list'),
    path('flashcards/create/', flashcard_views.flashcard_create, name='flashcard_create'),
    path('flashcards/<int:pk>/edit/', flashcard_views.flashcard_edit, name='flashcard_edit'),
    path('flashcards/<int:pk>/delete/', flashcard_views.flashcard_delete, name='flashcard_delete'),
    path('flashcards/shuffle/', flashcard_views.shuffle, name='shuffle'),
    path('flashcards/next/', flashcard_views.get_next_flashcard, name='get_next_flashcard'),
]