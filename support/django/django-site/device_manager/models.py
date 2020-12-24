from django.db import models


class Fleet(models.Model):

    name = models.CharField(max_length=255)
    api_key = models.CharField(max_length=255)
    endpoint = models.URLField(max_length=255, default="")
    dashboard = models.URLField(max_length=255, default="")
    cluster_local = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Device(models.Model):

    id = models.CharField(max_length=255, primary_key=True)
    device_class = models.CharField(max_length=255, verbose_name="class")
    provisioning_data = models.JSONField()
    fleet = models.ForeignKey(Fleet, on_delete=models.deletion.CASCADE)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.id


class ReceivedData(models.Model):

    device = models.ForeignKey(Device, on_delete=models.deletion.CASCADE)
    data = models.JSONField()
    timestamp = models.DateTimeField()

    class Meta:
        verbose_name_plural = "received data"
