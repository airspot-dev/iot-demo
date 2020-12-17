from django.apps import AppConfig


class DeviceManagerAppConfig(AppConfig):
    name = 'device_manager'
    verbose_name = 'Device Manager'

    def ready(self):
        from .models import Device, Fleet
        from django_signals_cloudevents import send_cloudevent
        from django.db.models.signals import post_save, post_delete
        post_save.connect(send_cloudevent, sender=Fleet)
        post_delete.connect(send_cloudevent, sender=Fleet)
        post_save.connect(send_cloudevent, sender=Device)
        post_delete.connect(send_cloudevent, sender=Device)
