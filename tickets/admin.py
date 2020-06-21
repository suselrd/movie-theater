from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Booking


class BookingAdmin(ModelAdmin):
    list_display = ('created', 'paid_amount', 'seats')


admin.site.register(Booking, BookingAdmin)
