from django.conf import settings
from django.db import models


class DayOfWeek(models.IntegerChoices):
    MONDAY = 1, "Понедельник"
    TUESDAY = 2, "Вторник"
    WEDNESDAY = 3, "Среда"
    THURSDAY = 4, "Четверг"
    FRIDAY = 5, "Пятница"
    SATURDAY = 6, "Суббота"
    SUNDAY = 7, "Воскресенье"


class WorkingHour(models.Model):
    """Регулярное недельное расписание мастера (шаблон графика работы)."""

    master = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="working_hours", verbose_name="Мастер"
    )
    day_of_week = models.IntegerField(choices=DayOfWeek.choices, verbose_name="День недели")
    start_time = models.TimeField(verbose_name="Время начала")
    end_time = models.TimeField(verbose_name="Время окончания")
    is_day_off = models.BooleanField(default=False, verbose_name="Выходной день")

    class Meta:
        unique_together = ("master", "day_of_week")
        verbose_name = "Рабочие часы"
        verbose_name_plural = "Расписание работы"

    def __str__(self):
        return f"{self.master} - {self.get_day_of_week_display()}"


class TimeOff(models.Model):
    """Исключения из графика: отпуска, больничные, разовые выходные."""

    master = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Мастер")
    start_date = models.DateField(verbose_name="Дата начала")
    end_date = models.DateField(verbose_name="Дата окончания")
    reason = models.CharField(max_length=100, blank=True, verbose_name="Причина (опционально)")

    class Meta:
        verbose_name = "Исключение из расписания (Отгул)"
        verbose_name_plural = "Исключения из расписания"

    def __str__(self):
        return f"{self.master} ({self.start_date} - {self.end_date})"


class AppointmentStatus(models.TextChoices):
    PENDING = "pending", "Ожидает"
    IN_PROGRESS = "in_progress", "В работе"
    COMPLETED = "completed", "Завершен"
    CANCELLED = "cancelled", "Отменен"


class Appointment(models.Model):
    """Журнал записей клиентов (Ядро системы)."""

    master = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="appointments", verbose_name="Мастер"
    )
    customer = models.ForeignKey(
        "customers.Customer",
        on_delete=models.PROTECT,
        related_name="appointments",
        verbose_name="Клиент",
    )
    services = models.ManyToManyField("catalog.Service", verbose_name="Услуга")

    start_time = models.DateTimeField(db_index=True, verbose_name="Время начала записи")
    end_time = models.DateTimeField(db_index=True, verbose_name="Время окончания записи")

    status = models.CharField(
        max_length=20, choices=AppointmentStatus.choices, default=AppointmentStatus.PENDING, verbose_name="Статус"
    )

    customer_comment = models.TextField(blank=True, null=True, verbose_name="Комментарий клиента")
    internal_notes = models.TextField(blank=True, null=True, verbose_name="Заметки мастера (скрыто)")

    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Журнал записей"
        ordering = ["-start_time"]

    def __str__(self):
        return f"Запись {self.customer} к {self.master} на {self.start_time.strftime('%d.%m.%Y %H:%M')}"
