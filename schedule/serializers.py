from datetime import timedelta

from django.db.models import Q
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Showtime


class ShowtimeSerializer(serializers.ModelSerializer):
    room_url = serializers.HyperlinkedRelatedField(source='room', view_name='room-detail', read_only=True)
    movie_url = serializers.HyperlinkedRelatedField(source='movie', view_name='movie-detail', read_only=True)

    class Meta:
        model = Showtime
        fields = ('url', 'pk', 'room', 'room_url', 'movie', 'movie_url', 'start', 'end', 'price')
        read_only_fields = ('end',)

    def validate(self, attrs):
        end = attrs['start'] + timedelta(minutes=attrs['movie'].duration)
        qs = attrs['room'].showtime_set
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.filter(
            Q(start__lte=attrs['start'], end__gte=attrs['start']) |
            Q(start__lte=end, end__gte=end) |
            Q(start__gte=attrs['start'], end__lte=end)
        ).exists():
            raise ValidationError('Can not schedule this movie, the room is being used.')
        return attrs
