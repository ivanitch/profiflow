# apps/locations/services.py
from django.conf import settings

from .providers import DaDataProvider, LocalDatabaseProvider, LocationProvider


def get_location_provider() -> LocationProvider:
    provider_name = getattr(settings, "LOCATION_PROVIDER", "local")

    if provider_name == "dadata":
        return DaDataProvider()

    return LocalDatabaseProvider()
