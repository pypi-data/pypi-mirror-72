from rest_framework.viewsets import ModelViewSet
from plugin.models import DeviceInfo
from plugin.api.serializers import DeviceSerializer


class DeviceViewSet(ModelViewSet):
    """
    View, create, update, or delete device
    """
    queryset = DeviceInfo.objects.all()
    serializer_class = DeviceSerializer