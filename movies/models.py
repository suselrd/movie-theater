import logging

from django.db import models
from django.utils.translation import ugettext as _

logger = logging.getLogger(__name__)


class Movie(models.Model):
    title = models.CharField(_('title'), max_length=1000)
    duration = models.PositiveSmallIntegerField(_('duration'), help_text=_('duration in minutes'))

    class Meta:
        verbose_name = _("movie")
        verbose_name_plural = _("movies")
        ordering = ('title',)

    def __str__(self):
        return self.title
