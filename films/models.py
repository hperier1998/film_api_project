# films/models.py

from django.db import models


class Film(models.Model):
    """
    Model representing a film.
    """

    name = models.CharField(max_length=128, help_text="Enter the name of the film")
    description = models.TextField(max_length=2048, help_text="Enter a brief description of the film")
    publication_date = models.DateField(help_text="Enter the publication date of the film in ISO 8601 format")
    note = models.IntegerField(default=0, blank=True, null=True, help_text="Enter the note of the film (optional)")

    # Additional fields can be added here as needed

    def __str__(self):
        """
        String for representing the Film object.
        """
        return self.name
