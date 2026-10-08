import datetime
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView, View
from django.http import JsonResponse
from django.contrib import messages
from django.utils.timezone import make_aware
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.timezone import localdate

from apps.users.models import MasterProfile
from apps.catalog.models import Service
from apps.customers.models import Customer
from apps.booking.models import Appointment


class PublicBookingWidgetView(TemplateView):
    """Публичная страница (виджет) записи к мастеру."""
    template_name = "booking/appointment.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        master_profile = get_object_or_404(MasterProfile, booking_slug=self.kwargs['booking_slug'])

        context['master'] = master_profile.user
        context['master_profile'] = master_profile
        # Достаем услуги мастера
        context['services'] = Service.objects.filter(
            master=master_profile.user,
            is_deleted=False
        ).select_related('category')

        # Генерация 14 дней (начиная с сегодня) для скролла дат
        today = localdate()
        months_ru = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь",
                     "Ноябрь", "Декабрь"]
        days_ru = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]

        dates = []
        for i in range(14):
            d = today + datetime.timedelta(days=i)
            dates.append({
                "iso": d.strftime("%Y-%m-%d"),
                "day": d.day,
                "weekday": days_ru[d.weekday()],
                "month_name": f"{months_ru[d.month - 1]} {d.year}",
            })

        context['available_dates'] = dates
        return context


class AvailableSlotsAPIView(View):
    """
    API эндпоинт для подгрузки свободного времени по выбранной дате и услуге.
    """

    def get(self, request, booking_slug):
        date_str = request.GET.get('date')
        service_id = request.GET.get('service_id')

        if not date_str or not service_id:
            return JsonResponse({"error": "Missing parameters"}, status=400)

        # TODO: Здесь будет сложный алгоритм генерации слотов на основе
        # WorkingHour, TimeOff и существующих Appointment.
        # Пока отдаем жестко заданные часы для тестирования фронтенда.

        mock_slots = [
            {"time": "10:00", "available": False},
            {"time": "11:00", "available": True},
            {"time": "13:30", "available": True},
            {"time": "15:00", "available": True},
        ]

        return JsonResponse({"slots": mock_slots})


class CreateAppointmentView(View):
    """
    Обработчик формы создания записи от клиента.
    """

    def post(self, request, booking_slug):
        master_profile = get_object_or_404(MasterProfile, booking_slug=booking_slug)
        master = master_profile.user

        # 1. Извлекаем данные из POST-запроса
        service_id = request.POST.get('service_id')
        date_str = request.POST.get('date')
        time_str = request.POST.get('time')
        first_name = request.POST.get('first_name')
        phone = request.POST.get('phone')
        comment = request.POST.get('comment', '')

        # Базовая защита от пустых данных (на случай если JS на фронте отключен)
        if not all([service_id, date_str, time_str, first_name, phone]):
            messages.error(request, "Пожалуйста, заполните все обязательные поля.")
            return redirect('public_booking:widget', booking_slug=booking_slug)

        try:
            # 2. Получаем услугу и вычисляем время окончания
            service = get_object_or_404(Service, id=service_id, master=master, is_deleted=False)

            """
            Собираем datetime (с учетом того, что это локальное время мастера
            - в идеале привязывать к таймзоне из MasterProfile)
            """
            start_datetime_naive = datetime.datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
            start_datetime = make_aware(start_datetime_naive)
            end_datetime = start_datetime + datetime.timedelta(minutes=service.duration)

            # 3. CRM: Ищем существующего клиента по номеру или создаем нового
            customer, created = Customer.objects.get_or_create(
                master=master,
                phone=phone,
                defaults={'first_name': first_name}
            )

            # Если клиент уже был, но сменил имя, можно обновить его здесь

            # 4. Создаем запись
            Appointment.objects.create(
                master=master,
                customer=customer,
                service=service,
                start_time=start_datetime,
                end_time=end_datetime,
                customer_comment=comment
            )

            # 5. Уведомляем клиента об успехе
            messages.success(request, f"Вы успешно записаны на {date_str} в {time_str}!")

            # TODO: Вызов Celery таски для отправки Telegram-уведомления мастеру

        except ValueError:
            messages.error(request, "Неверный формат даты или времени.")
        except Exception as e:
            messages.error(request, "Произошла системная ошибка. Попробуйте позже.")

        # Возвращаем клиента на страницу виджета
        return redirect('public_booking:widget', booking_slug=booking_slug)


class MasterDashboardView(LoginRequiredMixin, TemplateView):
    """
    Главный экран дашборда мастера (Канбан-доска).
    Доступен только авторизованным мастерам.
    """
    # Временно используем demo.html как заглушку. Позже заменим на реальный шаблон.
    template_name = "base.html"


class MasterCalendarView(LoginRequiredMixin, TemplateView):
    """
    Календарь записей (Таймлайн) для мастера.
    """
    template_name = "base.html"


class ScheduleSettingsView(LoginRequiredMixin, TemplateView):
    """
    Настройки регулярного расписания и выходных дней.
    """
    template_name = "base.html"
