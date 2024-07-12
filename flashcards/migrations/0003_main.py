from django.db import migrations, models
import django.db.models.deletion

def create_default_deck_and_associate_flashcards(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Deck = apps.get_model('flashcards', 'Deck')
    Flashcard = apps.get_model('flashcards', 'Flashcard')

    for user in User.objects.all():
        default_deck, created = Deck.objects.get_or_create(user=user, name="Default Deck")
        Flashcard.objects.filter(user=user, deck__isnull=True).update(deck=default_deck)

class Migration(migrations.Migration):

    dependencies = [
        ('flashcards', '0002_main'),
    ]

    operations = [
        migrations.CreateModel(
            name='Deck',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
        migrations.AddField(
            model_name='flashcard',
            name='deck',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='flashcards', to='flashcards.deck'),
        ),
        migrations.RunPython(create_default_deck_and_associate_flashcards),
    ]