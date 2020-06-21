from django.utils.translation import ugettext as _
from rest_framework import serializers

from .models import Booking


class BookingSerializer(serializers.ModelSerializer):
    showtime_url = serializers.HyperlinkedRelatedField(source='showtime', view_name='showtime-detail', read_only=True)

    class Meta:
        model = Booking
        fields = ('url', 'pk', 'created', 'paid_amount', 'showtime', 'showtime_url', 'seats')

    def validate(self, data):
        if data['seats'] > data['showtime'].available_seats:
            raise serializers.ValidationError(_('There is not enough seats available'))
        return data
