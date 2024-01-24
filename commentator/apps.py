from django.apps import AppConfig


class CommentatorConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "commentator"

    def ready(self):
        import commentator.signals
