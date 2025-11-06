def global_settings(request):
    """
    Context processor para variables globales
    """
    context = {
        'app_name': 'Sistema de Gestión',
        'app_version': '1.0.0',
    }
    
    if request.user.is_authenticated:
        context['user_permissions'] = {
            'can_manage_users': request.user.is_superuser,
            'can_view_dashboard': True,
        }
    
    return context