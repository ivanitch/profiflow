from django.shortcuts import redirect
from django.views import View


class IndexRedirectView(View):
    """
    Умный редирект с корня сайта.
    """

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard:home')
        return redirect('users:login')
