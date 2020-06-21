import pytest
from rest_framework import status
from rest_framework.reverse import reverse

# noinspection PyUnresolvedReferences
from schedule.tests import showtime, room, movie
from .models import Booking


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    client = APIClient(enforce_csrf_checks=True)
    return client


@pytest.fixture
def booking(showtime):
    booking_example = Booking(
        showtime=showtime
    )

    booking_example.save()
    return booking_example


@pytest.fixture
def booking_queryset(showtime):
    for i in range(5):
        booking_i = Booking(
            showtime=showtime
        )
        booking_i.save()
    return Booking.objects.all()


@pytest.mark.django_db
class TestModel:

    def test_booking_unicode(self, booking):
        assert str(booking) == '%(showtime)s - %(seats)s' % {
            'showtime': booking.showtime,
            'seats': booking.seats
        }

    def test_booking_seats_default(self, booking):
        assert booking.seats == 1

    def test_booking_total_calculation(self, booking):
        assert booking.paid_amount == booking.seats * booking.showtime.price


@pytest.mark.django_db
class TestViews:

    def test_booking_view_set_get_list(self, api_client, booking_queryset):
        """Test the BookingViewSet bookings list."""
        response = api_client.get(reverse('booking-list'), format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == len(booking_queryset)

    def test_booking_view_set_get_detail(self, api_client, booking):
        """Test the BookingViewSet booking detail."""
        url = reverse('booking-detail', kwargs={'pk': booking.pk})
        response = api_client.get(url, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['showtime_url'].endswith(reverse('showtime-detail', kwargs={'pk': booking.showtime.pk}))
        assert response.data['showtime'] == booking.showtime.pk
        assert response.data['seats'] == booking.seats
        assert 'paid_amount' in response.data
        assert 'created' in response.data

    def test_booking_view_set_post(self, api_client, showtime):
        """Test the BookingViewSet booking creation."""
        data = {
            "showtime": showtime.pk,
            "seats": 2
        }
        response = api_client.post(reverse('booking-list'), data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Booking.objects.count() == 1
        booking = Booking.objects.first()
        assert booking.showtime.pk == data['showtime']
        assert booking.seats == data['seats']

    def test_booking_view_set_post_not_enough_seats(self, api_client, showtime):
        """Test the BookingViewSet booking creation failure when there is not enough seats."""
        data = {
            "showtime": showtime.pk,
            "seats": 200
        }
        response = api_client.post(reverse('booking-list'), data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
