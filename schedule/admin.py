from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Showtime


class ShowtimeAdmin(ModelAdmin):
    list_display = ('room', 'movie', 'start', 'end', 'price')
    search_fields = ('room__name', 'movie__title')


admin.site.register(Showtime, ShowtimeAdmin)
