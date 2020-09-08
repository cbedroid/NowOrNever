from django.apps import AppConfig


class CountrycuzzinsConfig(AppConfig):
    name = "countrycuzzins"

    def ready(self):
        import countrycuzzins.signals
