from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import ClientProfile, MasterProfile, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Расширенная админка для нашей кастомной модели User.
    Убрано поле username, упор на email.
    """

    list_display = ("email", "phone", "is_staff", "is_active")
    search_fields = ("email", "phone")
    ordering = ("email",)

    # Переопределяем fieldsets для страницы РЕДАКТИРОВАНИЯ
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("phone",)}),
        (
            _("Permissions"),
            {
                "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions"),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )

@admin.register(MasterProfile)
class MasterProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "booking_slug", "city", "is_onboarding_completed")
    list_filter = ("is_onboarding_completed", "city")
    search_fields = ("user__email", "booking_slug")
    autocomplete_fields = ("user", "city")


@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "first_name", "last_name", "city")
    search_fields = ("user__email", "first_name", "last_name")
    autocomplete_fields = ("user", "city")
