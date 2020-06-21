from rest_framework import serializers

from .models import Showtime


class ShowtimeSerializer(serializers.ModelSerializer):
    room_url = serializers.HyperlinkedRelatedField(source='room', view_name='room-detail', read_only=True)
    movie_url = serializers.HyperlinkedRelatedField(source='movie', view_name='movie-detail', read_only=True)

    class Meta:
        model = Showtime
        fields = ('url', 'pk', 'room', 'room_url', 'movie', 'movie_url', 'start', 'end', 'price')
        read_only_fields = ('end',)
