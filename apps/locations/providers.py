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
        city, created = City.objects.get_or_create(
            name=name,
            region=region,
            defaults={"timezone": "Europe/Moscow"},
        )
        return city


class DaDataProvider(LocationProvider):
    """Phase 2: Идет в API DaData, обогащает данные и сохраняет в нашу БД."""

    def search_cities(self, query: str) -> list[dict]:
        raise NotImplementedError("Интеграция с DaData запланирована на Phase 2")

    def get_or_create_city(self, name: str, region: str | None = None) -> City:
        raise NotImplementedError("Интеграция с DaData запланирована на Phase 2")
