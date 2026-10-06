from django.contrib import admin

from .models import City


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    exclude = ("timezone",)
    readonly_fields = ("lat", "lon")
    search_fields = ("name", "region")
