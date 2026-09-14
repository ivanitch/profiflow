from django.shortcuts import render


def home_page(request):
    context = {
        'title': 'ProfiFlow — сервис онлайн-записи для бьюти-мастеров и студий.',
        'h1': 'ProfiFlow',
    }
    return render(request, 'main/home.html', context)
