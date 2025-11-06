from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta

@login_required
def dashboard(request):
    # Estadísticas de usuarios
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    superusers = User.objects.filter(is_superuser=True).count()
    
    # Usuarios registrados en los últimos 30 días
    last_30_days = timezone.now() - timedelta(days=30)
    recent_users = User.objects.filter(date_joined__gte=last_30_days).count()
    
    # Datos para gráficos
    # Usuarios por mes (últimos 6 meses)
    months_data = []
    users_per_month = []
    for i in range(5, -1, -1):
        month_start = timezone.now() - timedelta(days=30*i)
        month_end = timezone.now() - timedelta(days=30*(i-1)) if i > 0 else timezone.now()
        count = User.objects.filter(
            date_joined__gte=month_start,
            date_joined__lt=month_end
        ).count()
        months_data.append(month_start.strftime('%b %Y'))
        users_per_month.append(count)
    
    # Últimos usuarios registrados
    latest_users = User.objects.order_by('-date_joined')[:5]
    
    context = {
        'now': timezone.now(),
        'total_users': total_users,
        'active_users': active_users,
        'superusers': superusers,
        'recent_users': recent_users,
        'months_data': months_data,
        'users_per_month': users_per_month,
        'latest_users': latest_users,
    }
    
    return render(request, 'dashboard/index.html', context)