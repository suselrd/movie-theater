from rest_framework import serializers

from schedule.models import Showtime
from .models import Room


class RoomShowtimeSerializer(serializers.ModelSerializer):
    movie = serializers.StringRelatedField()
    is_playing = serializers.SerializerMethodField()

    class Meta:
        model = Showtime
        fields = ('movie', 'start', 'price', 'is_playing')

    def get_is_playing(self, obj):
        return obj.is_playing


class RoomSerializer(serializers.HyperlinkedModelSerializer):
    upcoming_showtimes = RoomShowtimeSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = ('url', 'pk', 'name', 'capacity', 'upcoming_showtimes')
