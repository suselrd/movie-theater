"""main URL Configuration"""

from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from movies.urls import movies_router
from rooms.urls import rooms_router
from schedule.urls import showtimes_router
from tickets.urls import bookings_router
from .routers import MainRouter

router = MainRouter()
router.register_child(rooms_router)
router.register_child(movies_router)
router.register_child(showtimes_router)
router.register_child(bookings_router)

urlpatterns = [
    url(r'^api/session/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include(router.urls)),
    url(r'^admin/', admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
