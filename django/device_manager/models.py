from django.db import models
from django.contrib.postgres.fields import JSONField


class Fleet(models.Model):

    name = models.CharField(max_length=255)
    api_key = models.CharField(max_length=255)
    endpoint = models.URLField(max_length=255, default="")
    status = models.CharField(max_length=255, default="UNKNOWN")


class Device(models.Model):

    name = models.CharField(max_length=255, primary_key=True)
    device_class = models.CharField(max_length=255)
    data = JSONField()
