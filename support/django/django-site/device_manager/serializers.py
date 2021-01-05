from rest_framework import serializers
from .models import Fleet, Device, ReceivedData


class FleetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Fleet
        fields = [
            'name', 'api_key', 'endpoint', 'dashboard', 'cluster_local',
        ]


class DeviceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Device
        fields = [
            'id', 'device_class', 'provisioning_data', 'fleet', 'status',
        ]


class ReceivedDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReceivedData
        fields = [
            'device', 'data', 'timestamp',
        ]
