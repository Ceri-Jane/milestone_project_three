# ---------------------------------------------------------------
# ACCOUNTS APP CONFIG
# - Registers this Django app and its settings.
# - 'ready()' runs when Django starts up.
# - Importing accounts.signals here ensures all signal handlers
#   (e.g., profile creation, email updates, etc.) are loaded
#   automatically when the project boots.
# ---------------------------------------------------------------

from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        import accounts.signals
