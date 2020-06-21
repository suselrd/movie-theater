from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Room


class RoomAdmin(ModelAdmin):
    list_display = ('name', 'capacity')
    search_fields = ('name',)


admin.site.register(Room, RoomAdmin)
