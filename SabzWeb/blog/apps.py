from django.apps import AppConfig


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
    # To change the name of the application in the Django panel.
    verbose_name = 'وبلاگ'
