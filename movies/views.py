from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from .models import Movie
from .serializers import MovieSerializer


class MovieViewSet(
    viewsets.ModelViewSet
):
    """
    API endpoint that allows movies to be viewed or edited.
    """
    serializer_class = MovieSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('title',)
    queryset = Movie.objects.all()
