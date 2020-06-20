from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from .models import Room
from .serializers import RoomSerializer


class RoomViewSet(
    viewsets.ModelViewSet
):
    """
    API endpoint that allows rooms to be viewed or edited.
    """
    serializer_class = RoomSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    queryset = Room.objects.all()
