from main.routers import StandardRouter
from . import views

bookings_router = StandardRouter()

bookings_router.register('bookings', views.BookingViewSet, 'booking')
