from django.apps import AppConfig


class HardeningConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hardening'
    verbose_name = 'OS Hardening Assistant'
