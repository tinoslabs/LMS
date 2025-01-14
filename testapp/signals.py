from django.apps import AppConfig

class YourAppConfig(AppConfig):
    name = 'your_app_name'

    def ready(self):
        import testapp.signals