from django.shortcuts import render


def home_page(request):
    context = {
        'title': 'ProfiFlow - Home page',
        'h1': 'ProfiFlow H1',
    }
    return render(request, 'main/home.html', context)
