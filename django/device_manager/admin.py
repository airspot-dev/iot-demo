from django.contrib import admin
from django.contrib.postgres.fields import JSONField
from prettyjson import PrettyJSONWidget

from .models import Fleet, Device


@admin.register(Fleet)
class FleetAdmin(admin.ModelAdmin):
    readonly_fields = ["status", "endpoint"]
    formfield_overrides = {
        JSONField: {'widget': PrettyJSONWidget(attrs={"initial": "parsed"})},
    }


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    pass
