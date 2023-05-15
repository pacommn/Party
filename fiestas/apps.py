from django.apps import AppConfig


class FiestasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fiestas'

    def ready(self):
        import fiestas.signals