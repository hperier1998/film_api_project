from django.db import migrations
from django.utils import timezone
from faker import Faker
from films.models.Film import Film
from films.models.Category import Category


def populate_data(apps, schema_editor):
    fake = Faker()
    films_to_create = 100

    for _ in range(films_to_create):
        name = fake.name()
        description = fake.text(max_nb_chars=200)
        publication_date = fake.date_between(start_date='-30y', end_date='today')
        note = fake.random_element(elements=[0, 1, 2, 3, 4, 5])

        Film.objects.create(
            name=name,
            description=description,
            publication_date=publication_date,
            note=note
        )


def reverse_data_populate(apps, schema_editor):
    Film.objects.filter(name='Example Film').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_data, reverse_code=reverse_data_populate),
    ]
