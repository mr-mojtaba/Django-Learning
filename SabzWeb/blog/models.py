from django.db import models

# Standard python library.
from django.utils import timezone
from django.contrib.auth.models import User


# Managers
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


# Create your models here.
class Post(models.Model):
    # Creating a class for posts status.
    class Status(models.TextChoices):
        DRAFT = ' DR', 'Draft'
        PUBLISHED = 'PB', 'Published'
        REJECTED = 'RJ', 'Rejected'

    # Creating a many-to-one field for user.
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_posts"
    )

    # To create fields.
    title = models.CharField(max_length=250)
    description = models.TextField()
    slug = models.SlugField(max_length=250)

    # Date of publication.
    publish = models.DateTimeField(default=timezone.now)

    # Recording the moment the post was created.
    created = models.DateTimeField(auto_now_add=True)

    # Date of update.
    updated = models.DateTimeField(auto_now=True)

    # Creating a field for Status class.
    status = models.CharField(
        max_length=250,
        choices=Status.choices,
        default=Status.DRAFT
    )

    # Keeping the default manager(objects).
    objects = models.Manager()
    # Create object from PublishedManager.
    published = PublishedManager()

    class Meta:
        # Sorting the table by publish.
        ordering = ['-publish']
        # Specifying the indexing.
        indexes = [
            models.Index(fields=['-publish'])
        ]

    # Overwriting the method as the title.
    def __str__(self):
        return self.title
