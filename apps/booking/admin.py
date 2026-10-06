from django.contrib import admin

from .models import Appointment, TimeOff, WorkingHour


@admin.register(WorkingHour)
class WorkingHourAdmin(admin.ModelAdmin):
    search_fields = ("master",)


@admin.register(TimeOff)
class TimeOffAdmin(admin.ModelAdmin):
    search_fields = ("master",)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    search_fields = ("master",)
