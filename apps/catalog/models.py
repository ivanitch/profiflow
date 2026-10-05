from django.db import models
from django.conf import settings
from apps.core.models import SoftDeleteModel


class Category(SoftDeleteModel):
    master = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='categories'
    )
    name = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0, help_text="Для ручной сортировки")

    class Meta:
        db_table = 'catalog_category'
        ordering = ['order', 'name']
        constraints = [
            # У мастера не может быть двух одинаковых АКТИВНЫХ категорий
            models.UniqueConstraint(
                fields=['master', 'name'],
                condition=models.Q(is_deleted=False),
                name='unique_active_category_per_master'
            )
        ]

    def __str__(self):
        return self.name


class Service(SoftDeleteModel):
    master = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='services'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,  # Если удалят категорию, услуга не удалится (станет "Без категории")
        null=True,
        blank=True,
        related_name='services'
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    # Финансовая часть и планирование
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    duration = models.PositiveIntegerField(default=60, help_text="Длительность в минутах")

    class Meta:
        db_table = 'catalog_service'
        ordering = ['category__order', 'name']
        indexes = [
            # Ускорит выборку активных услуг для конкретного мастера (для публичной страницы записи)
            models.Index(fields=['master', 'is_deleted']),
        ]

    def __str__(self):
        return self.name
