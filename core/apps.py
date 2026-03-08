# AppConfig stores metadata about the core app.
from django.apps import AppConfig


class CoreConfig(AppConfig):
    # Use big integers for automatically created primary keys.
    default_auto_field = 'django.db.models.BigAutoField'
    # This app is registered in Django under the name "core".
    name = 'core'
