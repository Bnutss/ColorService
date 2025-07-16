from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import timedelta
from reports.models import SupStorico, TuzRecord, SodaRecord, ColorServices


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        today = timezone.now().date()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)

        context['total_color_records'] = SupStorico.objects.count()
        context['total_salt_records'] = TuzRecord.objects.count()
        context['total_soda_records'] = SodaRecord.objects.count()
        context['total_products'] = ColorServices.objects.count()

        context['today_color_records'] = SupStorico.objects.filter(data_dosaggio__date=today).count()
        context['today_salt_records'] = TuzRecord.objects.filter(timestamp__date=today).count()
        context['today_soda_records'] = SodaRecord.objects.filter(timestamp__date=today).count()

        context['week_color_records'] = SupStorico.objects.filter(data_dosaggio__date__gte=week_ago).count()
        context['week_salt_records'] = TuzRecord.objects.filter(timestamp__date__gte=week_ago).count()
        context['week_soda_records'] = SodaRecord.objects.filter(timestamp__date__gte=week_ago).count()

        context['color_machines'] = SupStorico.objects.values('macchina').annotate(
            count=Count('sup_storico_id')).order_by('-count')[:5]
        context['salt_machines'] = TuzRecord.objects.values('makine_adi').annotate(count=Count('id')).order_by(
            '-count')[:5]
        context['soda_machines'] = SodaRecord.objects.values('makine_adi').annotate(count=Count('id')).order_by(
            '-count')[:5]

        context['recent_color_records'] = SupStorico.objects.order_by('-data_dosaggio')[:5]
        context['recent_salt_records'] = TuzRecord.objects.order_by('-timestamp')[:5]
        context['recent_soda_records'] = SodaRecord.objects.order_by('-timestamp')[:5]

        context['total_dosed_color'] = SupStorico.objects.aggregate(total=Sum('dosato'))['total'] or 0
        context['total_salt_kg'] = TuzRecord.objects.aggregate(total=Sum('miktar_kg'))['total'] or 0
        context['total_soda_kg'] = SodaRecord.objects.aggregate(total=Sum('miktar_kg'))['total'] or 0

        return context
