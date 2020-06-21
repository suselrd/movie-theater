from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Movie


class MovieAdmin(ModelAdmin):
    list_display = ('title', 'duration')
    search_fields = ('title',)


admin.site.register(Movie, MovieAdmin)
