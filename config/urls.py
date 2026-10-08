from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", include("apps.main.urls", namespace="main")),

    path("m/", include("apps.booking.urls.public", namespace="public_booking")),
    path("demo/", include("apps.demo.urls", namespace="demo")),

    # Личные кабинеты (Мастера и Клиенты)
    path("auth/", include("apps.users.urls", namespace="users")),
    path("dashboard/", include("apps.booking.urls.private", namespace="dashboard")),
    path("catalog/", include("apps.catalog.urls", namespace="catalog")),
    path("crm/", include("apps.customers.urls", namespace="customers")),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # type: ignore[arg-type]
