from django.apps import AppConfig


class AppcommerceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appcommerce'

    def ready(self):
        import appcommerce.signals