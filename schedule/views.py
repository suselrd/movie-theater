from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from .models import Showtime
from .serializers import ShowtimeSerializer


class ShowtimeViewSet(
    viewsets.ModelViewSet
):
    """
    API endpoint that allows showtimes to be viewed or edited.
    """
    serializer_class = ShowtimeSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('room__name', 'movie__title')
    queryset = Showtime.objects.all()
