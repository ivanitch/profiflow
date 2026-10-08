from django.urls import path
from apps.users import views

app_name = "users"

urlpatterns = [
    # Аутентификация
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("register/", views.RegisterView.as_view(), name="register"),  # Обновил имя класса на RegisterView
    path("logout/", views.UserLogoutView.as_view(), name="logout"),

    # Настройки профилей (Пока закомментируем, чтобы не ломался запуск)
    # path("settings/master/", views.MasterProfileEditView.as_view(), name="master_settings"),
    # path("settings/client/", views.ClientProfileEditView.as_view(), name="client_settings"),

    # Существующий View для профиля из твоего файла views.py
    path("profile/", views.UserProfileView.as_view(), name="profile"),
]
