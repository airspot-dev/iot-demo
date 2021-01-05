from django.db import models


class Fleet(models.Model):

    name = models.CharField(max_length=255, primary_key=True)
    api_key = models.CharField(max_length=255)
    endpoint = models.URLField(max_length=255, default="")
    dashboard = models.URLField(max_length=255, default="")
    cluster_local = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def delete(self, using=None, keep_parents=False):
        Device.objects.filter(fleet=self.name).delete()
        super().delete(using, keep_parents)


class Device(models.Model):

    id = models.CharField(max_length=255, primary_key=True)
    device_class = models.CharField(max_length=255, verbose_name="class")
    provisioning_data = models.JSONField()
    fleet = models.CharField(max_length=255)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.id

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if Fleet.objects.filter(name=self.fleet) == 0:
            raise Exception("Fleet with name %s does not exists" % self.fleet)
        super().save(force_insert, force_update, using, update_fields)

    def delete(self, using=None, keep_parents=False):
        ReceivedData.objects.filter(device=self.id).delete()
        super().delete(using, keep_parents)


class ReceivedData(models.Model):

    device = models.CharField(max_length=255)
    data = models.JSONField()
    timestamp = models.DateTimeField()

    class Meta:
        verbose_name_plural = "received data"

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if Device.objects.filter(name=self.device) == 0:
            raise Exception("Device with name %s does not exists" % self.device)
        super().save(force_insert, force_update, using, update_fields)
