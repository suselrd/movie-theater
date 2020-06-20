import logging
from django.db import models
from django.db.models import Case, Value, When
from django.utils import timezone
from django.utils.translation import ugettext as _


logger = logging.getLogger(__name__)


class Room (models.Model):
    name = models.CharField(_('name'), max_length=1000)
    capacity = models.PositiveSmallIntegerField(_('capacity'), help_text=_('number of seats'))

    class Meta:
        verbose_name = _("room")
        verbose_name_plural = _("rooms")
        ordering = ('name',)

    def __str__(self):
        return self.name

    @property
    def upcoming_showtimes(self):
        now = timezone.now()
        return self.showtime_set.filter(end__gte=now).annotate(
            is_playing=Case(
                When(start__lte=now,
                     then=Value(True)),
                default=Value(False),
                output_field=models.BooleanField()
            )
        )
