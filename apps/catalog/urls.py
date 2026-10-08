from django.urls import path
from apps.catalog import views

app_name = "catalog"

urlpatterns = [
    # Вывод всех услуг
    path("", views.ServiceListView.as_view(), name="list"),

    # Создание/редактирование
    path("create/", views.ServiceCreateView.as_view(), name="create"),
    path("<slug:slug>/edit/", views.ServiceUpdateView.as_view(), name="edit"),
    path("<slug:slug>/delete/", views.ServiceDeleteView.as_view(), name="delete"),  # Soft delete
]
