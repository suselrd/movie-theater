from datetime import timedelta

import pytest
from django.utils import timezone
from rest_framework import status
from rest_framework.reverse import reverse

# noinspection PyUnresolvedReferences
from movies.tests import movie, movie_queryset
# noinspection PyUnresolvedReferences
from rooms.tests import room, room_queryset
from .models import Showtime


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    client = APIClient(enforce_csrf_checks=True)
    return client


@pytest.fixture
def showtime(room, movie):
    showtime_example = Showtime(
        room=room,
        movie=movie,
        start=timezone.now() + timedelta(days=1),
        price=10.00
    )

    showtime_example.save()
    return showtime_example


@pytest.fixture
def showtime_queryset(room_queryset, movie_queryset):
    for i in range(5):
        showtime_i = Showtime(
            room=room_queryset[i],
            movie=movie_queryset[i],
            start=timezone.now() + timedelta(days=1),
            price=10.00
        )
        showtime_i.save()
    return Showtime.objects.all()


@pytest.mark.django_db
class TestModel:

    def test_showtime_unicode(self, showtime):
        """Test the string representation of Showtime Model."""
        assert str(showtime) == '%(movie)s - %(start)s - %(room)s' % {
            'movie': showtime.movie,
            'start': showtime.start,
            'room': showtime.room,
        }

    def test_showtime_end_calculation(self, showtime):
        assert showtime.end == showtime.start + timedelta(minutes=showtime.movie.duration)

    def test_showtime_initial_available_seats(self, showtime):
        assert showtime.available_seats == showtime.room.capacity


@pytest.mark.django_db
class TestViews:

    def test_showtime_view_set_get_list(self, api_client, showtime_queryset):
        """Test the ShowtimeViewSet showtimes list."""
        response = api_client.get(reverse('showtime-list'), format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == len(showtime_queryset)

    def test_showtime_view_set_search_list(self, api_client, showtime_queryset):
        """Test the ShowtimeViewSet showtimes list."""
        response = api_client.get(reverse('showtime-list'), format='json', data={'search': 'name'})
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == len(showtime_queryset)

        response = api_client.get(reverse('showtime-list'), format='json', data={'search': 'title'})
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == len(showtime_queryset)

        response = api_client.get(reverse('showtime-list'), format='json', data={'search': '1'})
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1

    def test_showtime_view_set_get_detail(self, api_client, showtime):
        """Test the ShowtimeViewSet showtime detail."""
        url = reverse('showtime-detail', kwargs={'pk': showtime.pk})
        response = api_client.get(url, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['room_url'].endswith(reverse('room-detail', kwargs={'pk': showtime.room.pk}))
        assert response.data['room'] == showtime.room.pk
        assert response.data['movie_url'].endswith(reverse('movie-detail', kwargs={'pk': showtime.movie.pk}))
        assert response.data['movie'] == showtime.movie.pk
        assert 'start' in response.data
        assert 'end' in response.data
        assert 'price' in response.data

    def test_showtime_view_set_put(self, api_client, showtime, room_queryset, movie_queryset):
        """Test the ShowtimeViewSet showtime update."""
        url = reverse('showtime-detail', kwargs={'pk': showtime.pk})
        new_room = room_queryset.exclude(pk=showtime.room.pk).first()
        new_movie = movie_queryset.exclude(pk=showtime.movie.pk).first()
        new_data = {
            "room": new_room.pk,
            "movie": new_movie.pk,
            "start": timezone.now() + timedelta(hours=2),
            "price": 20.00
        }
        response = api_client.put(url, new_data)
        assert response.status_code == status.HTTP_200_OK

        updated_showtime = Showtime.objects.get(pk=showtime.pk)
        assert updated_showtime.room == new_room
        assert updated_showtime.movie == new_movie
        assert updated_showtime.start == new_data['start']
        assert updated_showtime.end == new_data['start'] + timedelta(minutes=new_movie.duration)
        assert updated_showtime.price == new_data['price']

    def test_showtime_view_set_delete(self, api_client, showtime):
        """Test the ShowtimeViewSet showtime deletion."""
        url = reverse('showtime-detail', kwargs={'pk': showtime.pk})
        response = api_client.delete(url, format='json')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Showtime.objects.count() == 0

    def test_showtime_view_set_post(self, api_client, room, movie):
        """Test the ShowtimeViewSet showtime creation."""
        data = {
            "room": room.pk,
            "movie": movie.pk,
            "start": timezone.now() + timedelta(hours=2),
            "price": 10.00
        }
        response = api_client.post(reverse('showtime-list'), data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Showtime.objects.count() == 1
        showtime = Showtime.objects.first()
        assert showtime.room.pk == data['room']
        assert showtime.movie.pk == data['movie']
