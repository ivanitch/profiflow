from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from .models import Customer

class CustomerListView(LoginRequiredMixin, ListView):
    """
    Вывод списка клиентов мастера (CRM).
    """
    model = Customer
    template_name = "client_list.html"  # Тот самый шаблон со списком
    context_object_name = "customers"

    def get_queryset(self):
        # Строгая защита: мастер видит только своих клиентов
        return Customer.objects.filter(master=self.request.user).order_by('-created_at')


class CustomerDetailView(LoginRequiredMixin, DetailView):
    """
    Детальная карточка конкретного клиента с историей записей.
    """
    model = Customer
    template_name = "client_detail.html"  # Тот самый шаблон с профилем
    context_object_name = "client"

    def get_queryset(self):
        # Строгая защита: мастер может открыть только своего клиента
        return Customer.objects.filter(master=self.request.user)
