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
    email = models.EmailField(_("Email address"), unique=True)

    # Телефон оставляем здесь, так как он может использоваться для входа
    # в будущем (по SMS-коду) или системных уведомлений.
    phone = models.CharField(_("Phone number"), max_length=20, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()  # type: ignore[assignment,misc]

    class Meta:
        db_table = 'auth_user'
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.email


class MasterProfile(models.Model):
    """
    Бизнес-профиль мастера. Все публичные и настроечные данные лежат здесь.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    # Публичные данные (которые увидит клиент по ссылке)
    avatar = models.ImageField(_("Avatar"), upload_to="users/avatars/", blank=True, null=True)
    city = models.CharField(_("City"), max_length=100, blank=True, null=True, db_index=True)

    # Ссылка для онлайн-записи (profiflow.pro/m/anastasia)
    booking_slug = models.SlugField(max_length=100, unique=True, null=True, blank=True, db_index=True)

    # Локализация и финансы
    timezone = models.CharField(max_length=50, default='Asia/Yakutsk')
    currency = models.CharField(max_length=10, default='RUB')

    # Статус онбординга
    is_onboarding_completed = models.BooleanField(default=False)

    class Meta:
        db_table = 'users_master_profile'
        verbose_name = _("Master Profile")
        verbose_name_plural = _("Master Profiles")

    def __str__(self):
        return f"Профиль мастера: {self.user.email}"
