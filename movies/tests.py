import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from .models import Movie


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    client = APIClient(enforce_csrf_checks=True)
    return client


@pytest.fixture
def movie():
    movie_example = Movie(
        title='movie_title',
        duration=100,
    )

    movie_example.save()
    return movie_example


@pytest.fixture
def movie_queryset():
    for i in range(1, 6):
        movie_i = Movie(
            title='movie_title_%d' % i,
            duration=100 + i*10
        )
        movie_i.save()
    return Movie.objects.all()


@pytest.mark.django_db
class TestModel:

    def test_movie_unicode(self, movie):
        """Test the string representation of Movie Model."""
        assert str(movie) == movie.title


@pytest.mark.django_db
class TestViews:

    def test_movie_view_set_get_list(self, api_client, movie_queryset):
        """Test the MovieViewSet movies list."""
        response = api_client.get(reverse('movie-list'), format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == len(movie_queryset)

    def test_movie_view_set_search_list(self, api_client, movie_queryset):
        """Test the MovieViewSet movies list."""
        response = api_client.get(reverse('movie-list'), format='json', data={'search': 'title'})
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == len(movie_queryset)

        response = api_client.get(reverse('movie-list'), format='json', data={'search': '1'})
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1

    def test_movie_view_set_get_detail(self, api_client, movie):
        """Test the MovieViewSet movie detail."""
        url = reverse('movie-detail', kwargs={'pk': movie.pk})
        response = api_client.get(url, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == movie.title
        assert response.data['duration'] == movie.duration

    def test_movie_view_set_put(self, api_client, movie):
        """Test the MovieViewSet movie update."""
        url = reverse('movie-detail', kwargs={'pk': movie.pk})
        new_data = {
            "title": "new_title",
            "duration": 200,
        }
        response = api_client.put(url, new_data)
        assert response.status_code == status.HTTP_200_OK

        updated_movie = Movie.objects.get(pk=movie.pk)
        assert updated_movie.title == new_data['title']
        assert updated_movie.duration == new_data['duration']

    def test_movie_view_set_delete(self, api_client, movie):
        """Test the MovieViewSet movie deletion."""
        url = reverse('movie-detail', kwargs={'pk': movie.pk})
        response = api_client.delete(url, format='json')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Movie.objects.count() == 0

    def test_movie_view_set_post(self, api_client):
        """Test the MovieViewSet movie creation."""
        data = {
            "title": "new_title",
            "duration": 200,
        }
        response = api_client.post(reverse('movie-list'), data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Movie.objects.count() == 1
        movie = Movie.objects.first()
        assert movie.title == data['title']
        assert movie.duration == data['duration']
