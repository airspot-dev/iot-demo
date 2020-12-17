from django.db import models
from django.contrib.postgres.fields import JSONField


class Fleet(models.Model):

    name = models.CharField(max_length=255)
    api_key = models.CharField(max_length=255)
    endpoint = models.URLField(max_length=255, default="")
    status = models.CharField(max_length=255, default="UNKNOWN")


class Device(models.Model):

    id = models.CharField(max_length=255, primary_key=True)
    device_class = models.CharField(max_length=255, verbose_name="class")
    provisioning_data = JSONField()
    fleet = models.ForeignKey(Fleet, on_delete=models.deletion.CASCADE)
    status = models.BooleanField(default=False)


class ReceivedData(models.Model):

    device = models.ForeignKey(Device, on_delete=models.deletion.CASCADE)
    data = JSONField()
    timestamp = models.DateTimeField()
