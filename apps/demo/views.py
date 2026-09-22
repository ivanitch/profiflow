from django.shortcuts import render


def source_page(request):
    return render(request, 'demo/source.html')

def client_page(request):
    return render(request, 'demo/client.html')

def client_list_page(request):
    return render(request, 'demo/client_list.html')


# Appointment
def appointment_page(request):
    return render(request, 'demo/appointment.html')

def calendar_page(request):
    return render(request, 'demo/calendar.html')

def services_page(request):
    return render(request, 'demo/services.html')

