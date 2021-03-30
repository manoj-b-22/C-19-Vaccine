from django.apps import AppConfig


class C19VConfig(AppConfig):
    name = 'C19V'

    def ready(self):
        import C19V.signals