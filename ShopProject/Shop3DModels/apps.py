from django.apps import AppConfig


class Shop3DmodelsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Shop3DModels'

    def ready(self):
        import Shop3DModels.signals
