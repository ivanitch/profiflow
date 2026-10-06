# apps/locations/providers.py
from abc import ABC, abstractmethod

from .models import City


class LocationProvider(ABC):
    """Абстрактный интерфейс для поиска и валидации городов."""

    @abstractmethod
    def search_cities(self, query: str) -> list[dict]:
        """Возвращает список подсказок по введенному тексту."""
        pass

    @abstractmethod
    def get_or_create_city(self, name: str, region: str | None = None) -> City:
        """Возвращает объект City из БД или создает его, обогащая гео-данными."""
        pass


class LocalDatabaseProvider(LocationProvider):
    """Phase 1: Ищет только по нашей предзаполненной локальной базе."""

    def search_cities(self, query: str) -> list[dict]:
        cities = City.objects.filter(name__icontains=query)[:10]
        return [{"name": c.name, "region": c.region, "timezone": c.timezone} for c in cities]

    def get_or_create_city(self, name: str, region: str | None = None) -> City:
        # На старте мы просто берем город из базы. Если его нет - создаем болванку.
        city, created = City.objects.get_or_create(
            name=name,
            region=region,
            defaults={"timezone": "Europe/Moscow"},  # Фолбэк, если города не было в нашем JSON
        )
        return city


class DaDataProvider(LocationProvider):
    """Phase 2: Идет в API DaData, обогащает данные и сохраняет в нашу БД."""

    def search_cities(self, query: str) -> list[dict]:
        # Логика HTTP-запроса к dadata.ru/api/suggest/address
        # Возвращаем стандартизированный ответ
        pass

    def get_or_create_city(self, name: str, region: str | None = None) -> City:
        # 1. Ищем в локальной БД (чтобы не платить за API каждый раз)
        # 2. Если нет -> идем в DaData -> получаем timezone и координаты
        # 3. Сохраняем в локальную БД City.objects.create(...)
        # 4. Возвращаем объект
        pass
