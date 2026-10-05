from django.contrib import admin

from .models import MasterProfile, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    exclude = ("password",)
    readonly_fields = ("last_login", "date_joined")
    search_fields = ("email",)


@admin.register(MasterProfile)
class MasterProfileAdmin(admin.ModelAdmin):
    readonly_fields = ("timezone", "currency", "is_onboarding_completed")
    search_fields = ("city", "user")
