from main.routers import StandardRouter
from . import views

movies_router = StandardRouter()

movies_router.register('movies', views.MovieViewSet, 'movie')
