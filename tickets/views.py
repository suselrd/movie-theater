from rest_framework import viewsets, mixins

from .models import Booking
from .serializers import BookingSerializer


class BookingViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """
    API endpoint that allows movies to be viewed or edited.
    """
    serializer_class = BookingSerializer
    queryset = Booking.objects.all()
