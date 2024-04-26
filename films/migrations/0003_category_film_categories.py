from django.db import migrations, models
from films.models import Film, Category
import random


def populate_categories(apps, schema_editor):
    Category = apps.get_model('films', 'Category')
    Category.objects.bulk_create([
        Category(name='Action'),
        Category(name='Comedy'),
        Category(name='Drama'),
        Category(name='Horror'),
        Category(name='Romance'),
        Category(name='Thriller'),
        Category(name='Fantasy'),
        Category(name='Documentary'),
        Category(name='Crime'),
        Category(name='Science Fiction'),
    ])


def assign_categories_to_films(apps, schema_editor):
    # Retrieve all films
    films = Film.objects.all()

    # Retrieve a random category
    categories = Category.objects.all()

    # Assign random categories to each film
    for film in films:
        num_categories = random.randint(1, 4)  # Choose a random number of categories between 1 and 3
        random_categories = random.sample(list(categories), num_categories)  # Select random categories
        film.categories.add(*random_categories)  # Assign categories to the film


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0002_auto_20240423_1336'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='film',
            name='categories',
            field=models.ManyToManyField(to='films.category'),
        ),

        migrations.RunPython(populate_categories),
        migrations.RunPython(assign_categories_to_films),
    ]
