from django.urls import path

from apps.booking import views

app_name = "dashboard"

urlpatterns = [
    # Главный экран (Канбан на сегодня)
    path("", views.MasterDashboardView.as_view(), name="home"),
    # Календарь записей (Таймлайн)
    path("calendar/", views.MasterCalendarView.as_view(), name="calendar"),
    # Настройки графика работы
    path("schedule/", views.ScheduleSettingsView.as_view(), name="schedule"),
]
