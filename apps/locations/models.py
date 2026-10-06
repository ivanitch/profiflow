from django.db import models

from apps.base.auto_slug import AutoSlugModel


class City(AutoSlugModel):
    """Справочник городов для гео-привязки, SEO и автоматического определения часового пояса."""

    name = models.CharField(max_length=100, db_index=True, verbose_name="Название города")
    region = models.CharField(
        max_length=150, blank=True, null=True, verbose_name="Регион/Область", help_text="Например: Амурская область"
    )
    timezone = models.CharField(max_length=50, default="Asia/Yakutsk", verbose_name="Часовой пояс")

    # Координаты для интеграции с картами
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, verbose_name="Широта")
    lon = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, verbose_name="Долгота")

    class Meta:
        db_table = "locations_city"
        verbose_name = "Город"
        verbose_name_plural = "Города"
        unique_together = ("name", "region")

    def __str__(self):
        return f"{self.name} ({self.region})" if self.region else self.name
