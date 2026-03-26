# members/apps.py

from django.apps import AppConfig
import os
import threading

class MembersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        # Evita que se ejecute 2 veces en modo desarrollo
        if os.environ.get('RUN_MAIN') != 'true':
            return

        import scanner_client
        threading.Thread(target=scanner_client.main, daemon=True).start()