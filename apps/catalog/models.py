from django.conf import settings
from django.db import models

from apps.base.models import SoftDeleteModel


class Category(SoftDeleteModel):
    """Категории услуг для структурирования прайс-листа мастера."""

    master = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="categories", verbose_name="Мастер"
    )
    name = models.CharField(max_length=100, verbose_name="Название категории")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок", help_text="Для ручной сортировки")

    class Meta:
        db_table = "catalog_category"
        verbose_name = "Категория услуг"
        verbose_name_plural = "Категории услуг"
        ordering = ["order", "name"]
        constraints = [
            models.UniqueConstraint(
                fields=["master", "name"],
                condition=models.Q(is_deleted=False),
                name="unique_active_category_per_master",
            )
        ]

    def __str__(self):
        return self.name


class Service(SoftDeleteModel):
    """Конкретная услуга мастера с ценой и длительностью."""

    master = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="services", verbose_name="Мастер"
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="services", verbose_name="Категория"
    )
    name = models.CharField(max_length=255, verbose_name="Название услуги")
    description = models.TextField(blank=True, verbose_name="Описание")

    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Цена")
    duration = models.PositiveIntegerField(default=60, verbose_name="Длительность", help_text="В минутах")

    @property
    def formatted_duration(self):
        hours = self.duration // 60
        minutes = self.duration % 60

        if hours and minutes:
            return f"{hours} ч {minutes} мин"
        elif hours:
            return f"{hours} ч"
        return f"{minutes} мин"

    class Meta:
        db_table = "catalog_service"
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

        ordering = ["category__order", "price", "name"]
        indexes = [
            models.Index(fields=["master", "is_deleted"]),
        ]

    def __str__(self):
        return self.name
