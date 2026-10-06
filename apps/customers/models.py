from django.conf import settings
from django.db import models

from apps.base.models import SoftDeleteModel


class Customer(SoftDeleteModel):
    """Карточка клиента внутри локальной CRM мастера"""

    master = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="crm_customers", verbose_name="Мастер"
    )
    client_profile = models.ForeignKey(
        "users.ClientProfile",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Профиль клиента (если зарегистрирован в системе)",
    )

    first_name = models.CharField(max_length=100, verbose_name="Имя")
    phone = models.CharField(max_length=20, db_index=True, verbose_name="Телефон")
    notes = models.TextField(blank=True, null=True, verbose_name="Заметки мастера")

    class Meta:
        db_table = "customers_customer"
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        # У одного мастера не должно быть двух клиентов с одним номером
        unique_together = ("master", "phone")

    def __str__(self):
        return f"{self.first_name} ({self.phone})"
