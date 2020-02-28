from django.apps import AppConfig


class CakesConfig(AppConfig):
    name = 'cakes'

    def ready(self):
        from cakes import signals
