"""
Переносимый абстрактный миксин для автоматической генерации уникального
слага (в т.ч. из кириллицы) на основе title/name или произвольного поля.

Использование:

    class Article(AutoSlugModel):
        title = models.CharField(max_length=255)

    # или с кастомным источником:
    class Product(AutoSlugModel):
        brand = models.CharField(max_length=100)
        model_name = models.CharField(max_length=100)

        def get_slug_source(self):
            return f"{self.brand} {self.model_name}"

Зависимость:
    uv add python-slugify
"""

from django.db import models
from slugify import slugify


class AutoSlugModel(models.Model):
    """Абстрактная база: добавляет поле slug и логику его автозаполнения."""

    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True,
        verbose_name="URL (slug)",
    )

    class Meta:
        abstract = True

    def get_slug_source(self) -> str:
        """Строка-источник для слага."""
        source = getattr(self, "title", None) or getattr(self, "name", None)
        return str(source) if source else str(self)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._generate_unique_slug()
        else:
            self.slug = slugify(self.slug)
        super().save(*args, **kwargs)

    def _generate_unique_slug(self) -> str:
        # Безопасное извлечение max_length для mypy
        slug_field = self._meta.get_field("slug")
        max_length = getattr(slug_field, "max_length", 255) or 255
        max_len = max_length - 15

        base_slug = slugify(self.get_slug_source())[:max_len].rstrip("-")
        if not base_slug:
            base_slug = "no-title"

        slug = base_slug
        counter = 1
        ModelClass = self.__class__

        # mypy не видит objects у абстрактной модели, подавляем предупреждение
        qs = ModelClass.objects.filter(slug=slug)  # type: ignore[attr-defined]
        if self.pk:
            qs = qs.exclude(pk=self.pk)

        while qs.exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
            qs = ModelClass.objects.filter(slug=slug)  # type: ignore[attr-defined]
            if self.pk:
                qs = qs.exclude(pk=self.pk)

        return slug
