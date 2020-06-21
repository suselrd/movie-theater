import logging
from datetime import timedelta

from django.db import models
from django.db.models.aggregates import Sum
from django.dispatch import receiver
from django.utils.translation import ugettext as _

from movies.models import Movie
from rooms.models import Room

logger = logging.getLogger(__name__)


class Showtime(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name=_('room'))
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name=_('movie'))
    start = models.DateTimeField(_('starts at'))
    end = models.DateTimeField(_('ends at'), editable=False)
    price = models.DecimalField(_('price per seat'), max_digits=4, decimal_places=2)

    class Meta:
        verbose_name = _("showtime")
        verbose_name_plural = _("showtimes")
        ordering = ('room', 'start')

    def __str__(self):
        return '%(movie)s - %(start)s - %(room)s' % {
            'movie': self.movie,
            'start': self.start,
            'room': self.room,
        }

    @property
    def available_seats(self):
        return self.room.capacity - (self.booking_set.all().aggregate(Sum('seats')).get('seats__sum') or 0)


# noinspection PyUnusedLocal
@receiver(models.signals.pre_save, sender=Showtime, dispatch_uid='calculate_end')
def calculate_end(instance, **kwargs):
    instance.end = instance.start + timedelta(minutes=instance.movie.duration)
