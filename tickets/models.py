import logging

from django.core.validators import MinValueValidator
from django.db import models
from django.dispatch import receiver
from django.utils.translation import ugettext as _

from schedule.models import Showtime

logger = logging.getLogger(__name__)


class Booking(models.Model):
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE, verbose_name=_('showtime'))
    created = models.DateTimeField(_('created at'), auto_now_add=True)
    paid_amount = models.DecimalField(_('paid amount'), max_digits=10, decimal_places=2, editable=False)
    seats = models.PositiveSmallIntegerField(
        _('seats'), blank=True, default=1, validators=(MinValueValidator(limit_value=1),)
    )

    class Meta:
        verbose_name = _("booking")
        verbose_name_plural = _("bookings")
        ordering = ('created',)

    def __str__(self):
        return '%(showtime)s - %(seats)s' % {
            'showtime': self.showtime,
            'seats': self.seats
        }


# noinspection PyUnusedLocal
@receiver(models.signals.pre_save, sender=Booking, dispatch_uid='calculate_total')
def calculate_total(instance, **kwargs):
    instance.paid_amount = instance.seats * instance.showtime.price
