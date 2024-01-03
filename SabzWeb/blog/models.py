from django.db import models

# Standard python library
from django.utils import timezone


# Create your models here.
class Post(models.Model):
    # Creating a class for posts status.
    class Status(models.TextChoices):
        DRAFT = ' DR', 'Draft'
        PUBLISHED = 'PB', 'Published'
        REJECTED = 'RJ', 'Rejected'

    # To create fields
    title = models.CharField(max_length=250)
    description = models.TextField()
    slug = models.SlugField(max_length=250)

    # Date of publication
    publish = models.DateTimeField(default=timezone.now)

    # Recording the moment the post was created
    created = models.DateTimeField(auto_now_add=True)

    # Date of update
    updated = models.DateTimeField(auto_now=True)

    # Creating a field for Status class.S
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.DRAFT
    )

    # Sorting the table by publish.
    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish'])
        ]

    # Overwriting the method as the title.
    def __str__(self):
        return self.title
