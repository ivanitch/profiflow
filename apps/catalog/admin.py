from django.contrib import admin

from .models import Category, Service


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "master", "order", "is_deleted")
    list_filter = ("is_deleted", "master")
    search_fields = ("name", "master__email")
    autocomplete_fields = ("master",)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "master", "category", "price", "duration", "is_deleted")
    list_filter = ("is_deleted", "master", "category")
    search_fields = ("name", "master__email")
    autocomplete_fields = ("master", "category")
