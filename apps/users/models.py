from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager["User"]):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_("The Email field must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Чистая модель авторизации. Только то, что нужно для входа и базового контакта.
    """

    username = None  # type: ignore[assignment]
    email = models.EmailField(_("Email"), unique=True)

    # Телефон оставляем здесь, так как он может использоваться для входа
    # в будущем (по SMS-коду) или системных уведомлений.
    phone = models.CharField(_("Телефон"), max_length=20, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()  # type: ignore[assignment,misc]

    class Meta:
        db_table = "auth_user"
        verbose_name = _("Пользователь")
        verbose_name_plural = _("Пользователи")

    def __str__(self):
        return self.email


class MasterProfile(models.Model):
    """
    Бизнес-профиль мастера. Все публичные и настроечные данные SaaS лежат здесь.
    """

    user = models.OneToOneField(
        "users.User", on_delete=models.CASCADE, related_name="profile", verbose_name="Пользователь"
    )

    first_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Имя")
    last_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Фамилия")
    avatar = models.ImageField(upload_to="users/masters/avatars/", blank=True, null=True, verbose_name="Аватар")

    city = models.ForeignKey("locations.City", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Город")
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name="Адрес (улица, дом, кабинет)")

    booking_slug = models.SlugField(
        max_length=100,
        unique=True,
        null=True,
        blank=True,
        db_index=True,
        verbose_name="URL для записи (slug)",
        help_text="Уникальная ссылка вида profiflow.pro/m/slug",
    )

    timezone = models.CharField(max_length=50, default="Asia/Yakutsk", verbose_name="Часовой пояс")
    currency = models.CharField(max_length=10, default="RUB", verbose_name="Валюта")
    is_onboarding_completed = models.BooleanField(default=False, verbose_name="Онбординг пройден")

    @property
    def short_name(self):
        """Возвращает имя (или 'Мастер' по умолчанию) и первую букву фамилии (например, 'Анастасия В.')"""
        name = self.first_name if self.first_name else "Мастер"

        if self.last_name:
            return f"{name} {self.last_name[:1]}."
        return name

    @property
    def full_name(self):
        """Возвращает имя (или 'Мастер' по умолчанию) и фамилию (например, 'Анастасия Власова')"""
        name = self.first_name if self.first_name else "Мастер"

        if self.last_name:
            return f"{name} {self.last_name}"
        return name

    class Meta:
        db_table = "users_master_profile"
        verbose_name = "Профиль мастера"
        verbose_name_plural = "Профили мастеров"

    def __str__(self):
        return f"Профиль мастера: {self.user.email}"


class ClientProfile(models.Model):
    """
    Личный кабинет зарегистрированного клиента.
    Сюда клиент заходит, чтобы посмотреть свои записи и любимых мастеров.
    """

    user = models.OneToOneField(
        "users.User", on_delete=models.CASCADE, related_name="client_profile", verbose_name="Пользователь"
    )
    first_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Имя")
    last_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Фамилия")
    avatar = models.ImageField(upload_to="users/clients/avatars/", blank=True, null=True, verbose_name="Аватар")

    city = models.ForeignKey("locations.City", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Город")

    favorites_masters = models.ManyToManyField(
        "users.MasterProfile", blank=True, related_name="favorited_by", verbose_name="Избранные мастера"
    )

    class Meta:
        db_table = "users_client_profile"
        verbose_name = "Профиль клиента"
        verbose_name_plural = "Профили клиентов"

    def __str__(self):
        return f"Клиент: {self.first_name} {self.last_name}".strip() or self.user.email
