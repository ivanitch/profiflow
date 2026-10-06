from django.contrib import admin

from .models import City


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("name", "region", "timezone", "slug")
    search_fields = ("name", "region")
    list_filter = ("timezone",)
    prepopulated_fields = {"slug": ("name",)}
