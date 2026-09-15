from django.urls import path
from .views import (
    source_page,
    home_page,
    client_page,
    client_list_page,
)

app_name = 'main'

urlpatterns = [
    path('', home_page, name='home'),
    path('source-page/', source_page, name='source-page'),
    path('client-page/', client_page, name='client-page'),
    path('client-list/', client_list_page, name='client-list'),
]
