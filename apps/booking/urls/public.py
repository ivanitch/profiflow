from django.urls import path

from apps.booking import views

app_name = "public_booking"

urlpatterns = [
    # Главная страница записи к конкретному мастеру
    path("<slug:booking_slug>/", views.PublicBookingWidgetView.as_view(), name="widget"),
    # Обработчик формы создания записи (POST)
    path("<slug:booking_slug>/book/", views.CreateAppointmentView.as_view(), name="create"),
    # API/AJAX эндпоинт для подгрузки свободных слотов при смене даты в календаре
    path("<slug:booking_slug>/api/slots/", views.AvailableSlotsAPIView.as_view(), name="api_slots"),
]
