from django.contrib import admin
from django.db.models import JSONField
from django_krules_procevents.widgets import ReadOnlyJSONWidget

from .models import Fleet, ReceivedData


@admin.register(Fleet)
class FleetAdmin(admin.ModelAdmin):
    readonly_fields = ["endpoint", "dashboard"]


@admin.register(ReceivedData)
class ReceivedDataAdmin(admin.ModelAdmin):
    list_display = ['owner', 'device', 'timestamp']
    search_fields = ['device']
    list_filter = ['owner']
    readonly_fields = ['device', 'owner', 'timestamp']
    formfield_overrides = {
        JSONField: {'widget': ReadOnlyJSONWidget()},
    }
