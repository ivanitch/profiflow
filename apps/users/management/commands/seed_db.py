# apps/users/management/commands/seed_db.py
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.booking.models import Appointment, AppointmentStatus
from apps.catalog.models import Category, Service
from apps.customers.models import Customer
from apps.locations.models import City
from apps.users.models import ClientProfile, MasterProfile, User


class Command(BaseCommand):
    help = "Наполняет БД первичными тестовыми данными (Seeding)"

    def handle(self, *args, **kwargs):
        self.stdout.write("Очистка старых данных...")
        # 1. Сначала удаляем объекты, которые ссылаются на юзеров (чтобы избежать ProtectedError)
        Appointment.objects.all().delete()
        Customer.objects.all().delete()
        Service.objects.all().delete()
        Category.objects.all().delete()

        # 2. Теперь можно безопасно удалять самих юзеров и города
        User.objects.exclude(is_superuser=True).delete()
        City.objects.all().delete()

        # 1. Город
        city = City.objects.create(name="Благовещенск", region="Амурская область", timezone="Asia/Yakutsk")

        # 2. Мастера (2 юзера)
        master1_user = User.objects.create_user(email="svetlana@test.com", password="password123", phone="+7140649936")
        MasterProfile.objects.create(
            user=master1_user,
            first_name="Светлана",
            last_name="Иванова",
            city=city,
            booking_slug="svetlana-nails",
            is_onboarding_completed=True,
        )

        master2_user = User.objects.create_user(
            email="irina-frolkina@test.com", password="password123", phone="+79992223344"
        )
        MasterProfile.objects.create(
            user=master2_user,
            first_name="Ирина",
            last_name="Фролкина",
            city=city,
            booking_slug="irina-frolkina",
            is_onboarding_completed=True,
        )

        # ==========================================
        # 3. Прайс-лист (Категории и Услуги)
        # ==========================================

        # --- МАСТЕР 1: СВЕТЛАНА (Ногти) ---
        cat_nails = Category.objects.create(master=master1_user, name="Маникюр", order=1)
        cat_pedicure = Category.objects.create(master=master1_user, name="Педикюр", order=2)
        cat_design = Category.objects.create(master=master1_user, name="Снятие и дизайн", order=3)

        # УСЛУГИ: МАНИКЮР
        srv_manicure = Service.objects.create(
            master=master1_user, category=cat_nails, name="Маникюр с покрытием гель лаком", price=1300, duration=180
        )
        Service.objects.create(
            master=master1_user, category=cat_nails, name="Маникюр без покрытия", price=800, duration=90
        )
        Service.objects.create(
            master=master1_user, category=cat_nails, name="Маникюр с укреплением ногтей", price=1400, duration=180
        )
        Service.objects.create(master=master1_user, category=cat_nails, name="Френч", price=200, duration=45)
        Service.objects.create(master=master1_user, category=cat_nails, name="Ремонт ногтя", price=250, duration=30)

        # УСЛУГИ: ПЕДИКЮР (Новые)
        Service.objects.create(
            master=master1_user, category=cat_pedicure, name="Педикюр с покрытием (полный)", price=1800, duration=120
        )
        Service.objects.create(
            master=master1_user, category=cat_pedicure, name="Педикюр (только пальчики)", price=1400, duration=90
        )
        Service.objects.create(
            master=master1_user, category=cat_pedicure, name="Педикюр без покрытия", price=1200, duration=60
        )

        # УСЛУГИ: СНЯТИЕ И ДИЗАЙН
        Service.objects.create(
            master=master1_user,
            category=cat_design,
            name="Снятие чужого материала без покрытия",
            price=400,
            duration=45,
        )
        Service.objects.create(
            master=master1_user,
            category=cat_design,
            name="Снятие чужого материала с покрытием",
            price=200,
            duration=45,
        )
        Service.objects.create(
            master=master1_user, category=cat_design, name="Снятие моего материала", price=0, duration=45
        )
        Service.objects.create(
            master=master1_user, category=cat_design, name="Наклейки, слайдеры, стемпинг", price=0, duration=45
        )
        Service.objects.create(master=master1_user, category=cat_design, name="Дизайн однотон", price=0, duration=60)

        # --- МАСТЕР 2: ИРИНА (Волосы) ---
        cat_hair = Category.objects.create(master=master2_user, name="Стрижки", order=1)
        cat_color = Category.objects.create(master=master2_user, name="Окрашивание", order=2)

        srv_haircut = Service.objects.create(
            master=master2_user, category=cat_hair, name="Мужская стрижка", price=1000, duration=60
        )
        srv_beard = Service.objects.create(
            master=master2_user, category=cat_hair, name="Оформление бороды", price=800, duration=45
        )
        Service.objects.create(master=master2_user, category=cat_hair, name="Женская стрижка", price=1500, duration=60)

        # Новые услуги окрашивания
        Service.objects.create(
            master=master2_user, category=cat_color, name="Сложное окрашивание (Airtouch)", price=6500, duration=240
        )
        Service.objects.create(
            master=master2_user, category=cat_color, name="Окрашивание корней", price=2000, duration=90
        )
        Service.objects.create(
            master=master2_user, category=cat_color, name="Консультация по цвету", price=0, duration=30
        )

        # 4. Клиенты (2 юзера)
        client1_user = User.objects.create_user(email="client1@test.com", password="password123", phone="+79990001111")
        client1_profile = ClientProfile.objects.create(
            user=client1_user, first_name="Иван", last_name="Петров", city=city
        )

        client2_user = User.objects.create_user(email="client2@test.com", password="password123", phone="+79990002222")
        client2_profile = ClientProfile.objects.create(
            user=client2_user, first_name="Елена", last_name="Смирнова", city=city
        )

        # 5. CRM Карточки клиентов (привязка к мастерам)
        crm_c1_m1 = Customer.objects.create(
            master=master1_user, client_profile=client1_profile, first_name="Иван", phone="+79990001111"
        )
        crm_c2_m1 = Customer.objects.create(
            master=master1_user, client_profile=client2_profile, first_name="Елена", phone="+79990002222"
        )
        crm_c1_m2 = Customer.objects.create(
            master=master2_user, client_profile=client1_profile, first_name="Иван", phone="+79990001111"
        )

        # 6. Записи (5 штук)
        now = timezone.now()

        # Записи к Анне
        appointment_1 = Appointment.objects.create(
            master=master1_user,
            customer=crm_c1_m1,
            start_time=now + timedelta(days=1, hours=10),
            end_time=now + timedelta(days=1, hours=12),
            status=AppointmentStatus.PENDING,
        )
        appointment_1.services.add(srv_manicure)

        appointment_2 = Appointment.objects.create(
            master=master1_user,
            customer=crm_c2_m1,
            start_time=now + timedelta(days=1, hours=13),
            end_time=now + timedelta(days=1, hours=15),
            status=AppointmentStatus.IN_PROGRESS,
        )
        appointment_2.services.add(srv_haircut)

        appointment_3 = Appointment.objects.create(
            master=master1_user,
            customer=crm_c2_m1,
            start_time=now - timedelta(days=2, hours=10),
            end_time=now - timedelta(days=2, hours=12),
            status=AppointmentStatus.COMPLETED,
        )
        appointment_3.services.add(srv_beard)

        # Записи к Ирине
        appointment_4 = Appointment.objects.create(
            master=master2_user,
            customer=crm_c1_m2,
            start_time=now + timedelta(days=2, hours=11),
            end_time=now + timedelta(days=2, hours=12),
            status=AppointmentStatus.PENDING,
        )
        appointment_4.services.add(srv_manicure)

        appointment_5 = Appointment.objects.create(
            master=master2_user,
            customer=crm_c1_m2,
            start_time=now + timedelta(days=2, hours=12),
            end_time=now + timedelta(days=2, hours=12, minutes=45),
            status=AppointmentStatus.PENDING,
        )
        appointment_5.services.add(srv_manicure)

        self.stdout.write(self.style.SUCCESS("БД успешно наполнена! (Пароли всех юзеров: password123)"))
