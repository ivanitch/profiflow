from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView
from .models import Service

class ServiceListView(LoginRequiredMixin, ListView):
    """
    Вывод списка услуг и категорий мастера (Прайс-лист).
    """
    model = Service
    # Укажи здесь путь к твоему шаблону services.html
    template_name = "services.html"
    context_object_name = "services"

    def get_queryset(self):
        # Мастер видит только свои не удаленные услуги
        return Service.objects.filter(
            master=self.request.user,
            is_deleted=False
        ).select_related('category')

# --- Заглушки для остальных маршрутов каталога, чтобы не падал urls.py ---

class ServiceCreateView(LoginRequiredMixin, TemplateView):
    template_name = "demo.html"

class ServiceUpdateView(LoginRequiredMixin, TemplateView):
    template_name = "demo.html"

class ServiceDeleteView(LoginRequiredMixin, TemplateView):
    template_name = "demo.html"
