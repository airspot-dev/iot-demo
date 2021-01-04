from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import FleetSerializer, DeviceSerializer, ReceivedDataSerializer
from .models import Fleet, Device, ReceivedData


class FleetViewSet(viewsets.ModelViewSet):

    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated, ]
    serializer_class = FleetSerializer
    queryset = Fleet.objects.all()


class DeviceViewSet(viewsets.ModelViewSet):

    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated, ]
    serializer_class = DeviceSerializer
    queryset = Device.objects.all()


class ReceivedDataViewSet(viewsets.ModelViewSet):

    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated, ]
    serializer_class = ReceivedDataSerializer
    queryset = ReceivedData.objects.all()
