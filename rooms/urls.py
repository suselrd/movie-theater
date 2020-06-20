from main.routers import StandardRouter
from . import views

rooms_router = StandardRouter()

rooms_router.register('rooms', views.RoomViewSet, 'room')
