import pytest
from datetime import timedelta
from django.utils import timezone
from rest_framework import status
from rest_framework.reverse import reverse
# noinspection PyUnresolvedReferences
from movies.tests import movie
from .models import Room


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    client = APIClient(enforce_csrf_checks=True)
    return client


@pytest.fixture
def room():
    room_example = Room(
        name='room_name',
        capacity=100,
    )

    room_example.save()
    return room_example


@pytest.fixture
def room_with_upcoming_showtime(room, movie):
    from schedule.models import Showtime
    showtime = Showtime(
        room=room,
        movie=movie,
        start=timezone.now() + timedelta(days=1),
        price=10
    )
    showtime.save()
    return room


@pytest.fixture
def room_with_playing_showtime(room, movie):
    from schedule.models import Showtime
    showtime = Showtime(
        room=room,
        movie=movie,
        start=timezone.now() - timedelta(minutes=movie.duration//2),
        price=10
    )
    showtime.save()
    return room


@pytest.fixture
def room_queryset():
    for i in range(1, 6):
        room_i = Room(
            name='room_name_%d' % i,
            capacity=i*100
        )
        room_i.save()
    return Room.objects.all()


@pytest.mark.django_db
class TestModel:

    def test_room_unicode(self, room):
        """Test the string representation of Room Model."""
        assert str(room) == room.name

    def test_room_upcoming_showtime(self, room_with_upcoming_showtime):
        showtimes = room_with_upcoming_showtime.upcoming_showtimes
        assert showtimes.count() == 1
        assert showtimes.first().is_playing is False

    def test_room_playing_showtime(self, room_with_playing_showtime):
        showtimes = room_with_playing_showtime.upcoming_showtimes
        assert showtimes.count() == 1
        assert showtimes.first().is_playing is True


@pytest.mark.django_db
class TestViews:

    def test_room_view_set_get_list(self, api_client, room_queryset):
        """Test the RoomViewSet rooms list."""
        response = api_client.get(reverse('room-list'), format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == len(room_queryset)

    def test_room_view_set_search_list(self, api_client, room_queryset):
        """Test the RoomViewSet rooms list."""
        response = api_client.get(reverse('room-list'), format='json', data={'search': 'name'})
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == len(room_queryset)

        response = api_client.get(reverse('room-list'), format='json', data={'search': '1'})
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1

    def test_room_view_set_get_detail(self, api_client, room):
        """Test the RoomViewSet room detail."""
        url = reverse('room-detail', kwargs={'pk': room.pk})
        response = api_client.get(url, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == room.name
        assert response.data['capacity'] == room.capacity

    def test_room_view_set_get_detail_upcoming_showtime(self, api_client, room_with_upcoming_showtime):
        """Test the RoomViewSet room detail."""
        url = reverse('room-detail', kwargs={'pk': room_with_upcoming_showtime.pk})
        response = api_client.get(url, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['upcoming_showtimes']) == 1
        assert response.data['upcoming_showtimes'][0]['is_playing'] is False

    def test_room_view_set_get_detail_playing_showtime(self, api_client, room_with_playing_showtime):
        """Test the RoomViewSet room detail."""
        url = reverse('room-detail', kwargs={'pk': room_with_playing_showtime.pk})
        response = api_client.get(url, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['upcoming_showtimes']) == 1
        assert response.data['upcoming_showtimes'][0]['is_playing'] is True

    def test_room_view_set_put(self, api_client, room):
        """Test the RoomViewSet room update."""
        url = reverse('room-detail', kwargs={'pk': room.pk})
        new_data = {
            "name": "new_name",
            "capacity": 200,
        }
        response = api_client.put(url, new_data)
        assert response.status_code == status.HTTP_200_OK

        updated_room = Room.objects.get(pk=room.pk)
        assert updated_room.name == new_data['name']
        assert updated_room.capacity == new_data['capacity']

    def test_room_view_set_delete(self, api_client, room):
        """Test the RoomViewSet room deletion."""
        url = reverse('room-detail', kwargs={'pk': room.pk})
        response = api_client.delete(url, format='json')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Room.objects.count() == 0

    def test_room_view_set_post(self, api_client):
        """Test the RoomViewSet room creation."""
        data = {
            "name": "new_name",
            "capacity": 200,
        }
        response = api_client.post(reverse('room-list'), data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Room.objects.count() == 1
        room = Room.objects.first()
        assert room.name == data['name']
        assert room.capacity == data['capacity']
