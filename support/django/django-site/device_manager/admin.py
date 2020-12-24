from django.contrib import admin
from django.db.models import JSONField
from prettyjson import PrettyJSONWidget

from .models import Fleet, Device, ReceivedData


@admin.register(Fleet)
class FleetAdmin(admin.ModelAdmin):
    readonly_fields = ["endpoint", "dashboard"]
    formfield_overrides = {
        JSONField: {'widget': PrettyJSONWidget(attrs={"initial": "parsed"})},
    }


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    readonly_fields = ["status"]
    formfield_overrides = {
        JSONField: {'widget': PrettyJSONWidget(attrs={"initial": "parsed"})},
    }


@admin.register(ReceivedData)
class DeviceAdmin(admin.ModelAdmin):
    formfield_overrides = {
        JSONField: {'widget': PrettyJSONWidget(attrs={"initial": "parsed"})},
    }