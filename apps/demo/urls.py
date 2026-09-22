from django.urls import path

from .views import (
    source_page,
    client_page,
    client_list_page,
    appointment_page,
    calendar_page,
    services_page,
)

app_name = 'demo'

urlpatterns = [
    path('source-page/', source_page, name='source-page'),
    path('client-page/', client_page, name='client-page'),
    path('client-list/', client_list_page, name='client-list'),
    path('appointment-page/', appointment_page, name='appointment-page'),
    path('calendar-page/', calendar_page, name='calendar-page'),
    path('services-page/', services_page, name='services-page'),
]
