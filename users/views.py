from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache


class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'users/login_page.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('users:dashboard')
            else:
                form.add_error(None, "Неправильное имя пользователя или пароль.")

        return render(request, 'users/login_page.html', {'form': form})


class LogoutView(View):
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('users:login')


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'mainmenu/dashboard.html'
