from django.urls import path

from apps.customers import views

app_name = "customers"

urlpatterns = [
    path("", views.CustomerListView.as_view(), name="list"),
    path("<int:pk>/", views.CustomerDetailView.as_view(), name="detail"),
]
