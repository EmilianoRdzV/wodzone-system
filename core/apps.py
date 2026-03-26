from django.apps import AppConfig


class MembersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        # El scanner_client.py se ejecuta como proceso separado
        # Corre: python3 scanner_client.py
        pass
