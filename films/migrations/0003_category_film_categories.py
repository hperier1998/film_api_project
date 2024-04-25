from django.db import migrations, models


def populate_categories(apps, schema_editor):
    Category = apps.get_model('films', 'Category')
    Category.objects.bulk_create([
        Category(name='Action'),
        Category(name='Comedy'),
        Category(name='Drama'),
        # Add more categories as needed
    ])


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
    ]
