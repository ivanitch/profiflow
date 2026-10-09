from datetime import timedelta

import pytest
from django.utils import timezone

from apps.booking.models import Appointment
from apps.catalog.models import Category, Service
from apps.customers.models import Customer
from apps.locations.models import City
from apps.users.models import ClientProfile, MasterProfile, User


@pytest.mark.django_db
def test_appointment_creation():
    """Тест проверяет всю цепочку связей: Город -> Мастер -> Услуга -> Клиент -> CRM -> Запись"""

    # 1. Базовые сущности
    city = City.objects.create(name="Тест-город")
    master_user = User.objects.create_user(email="master@test.com", password="123")
    MasterProfile.objects.create(user=master_user, city=city, booking_slug="test-slug")

    # 2. Услуги
    category = Category.objects.create(master=master_user, name="Стрижки")
    service = Service.objects.create(master=master_user, category=category, name="Фейд", price=1000, duration=60)

    # 3. Клиент и CRM-профиль
    client_user = User.objects.create_user(email="client@test.com", password="123")
    client_profile = ClientProfile.objects.create(user=client_user, first_name="Иван", city=city)
    crm_customer = Customer.objects.create(
        master=master_user, client_profile=client_profile, first_name="Иван", phone="12345"
    )

    # 4. Запись
    now = timezone.now()
    appointment = Appointment.objects.create(
        master=master_user,
        customer=crm_customer,
        start_time=now,
        end_time=now + timedelta(minutes=service.duration),
    )

    appointment.services.add(service)

    assert Appointment.objects.count() == 1
    assert appointment.master.email == "master@test.com"
    assert appointment.customer.first_name == "Иван"
    first_service = appointment.services.first()
    assert first_service is not None
    assert first_service.price == 1000
    assert appointment.status == "pending"
