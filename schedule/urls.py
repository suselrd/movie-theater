from main.routers import StandardRouter
from . import views

showtimes_router = StandardRouter()

showtimes_router.register('showtimes', views.ShowtimeViewSet, 'showtime')
