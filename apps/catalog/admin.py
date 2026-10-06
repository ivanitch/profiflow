from django.contrib import admin

from .models import Category, Service


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ("master",)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    search_fields = ("master", "category")
