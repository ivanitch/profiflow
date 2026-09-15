from django.shortcuts import render


def home_page(request):
    context = {
        'title': 'ProfiFlow 🦋 сервис онлайн-записи для бьюти-мастеров и студий',
        'h1': 'Hello, world! 👋',
    }

    return render(request, 'main/home.html', context)

def source_page(request):
    return render(request, 'main/source.html')

def client_page(request):
    return render(request, 'main/client.html')

def client_list_page(request):
    return render(request, 'main/client_list.html')


# Appointment
def appointment_page(request):
    return render(request, 'main/appointment.html')
