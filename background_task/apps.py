from django.apps import AppConfig


class BackgroundTasksAppConfig(AppConfig):
    from background_task import __version__ as version_info

    name = "background_task"
    verbose_name = "Background Tasks ({})".format(version_info)
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self):
        import background_task.signals  # noqa
