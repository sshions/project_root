from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from .forms import UserCreateForm, UserUpdateForm, UserProfileForm

def superuser_required(view_func):
    """Decorator to check if user is superuser"""
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.error(request, 'No tienes permisos para acceder a esta sección.')
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

@login_required
@superuser_required
def user_list(request):
    query = request.GET.get('q', '')
    users = User.objects.all()
    
    if query:
        users = users.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )
    
    users = users.order_by('-date_joined')
    
    context = {
        'users': users,
        'query': query,
    }
    return render(request, 'users/list.html', context)

@login_required
@superuser_required
def user_create(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Usuario {user.username} creado exitosamente.')
            return redirect('users:list')
    else:
        form = UserCreateForm()
    
    return render(request, 'users/create.html', {'form': form})

@login_required
@superuser_required
def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'users/detail.html', {'user_obj': user})

@login_required
@superuser_required
def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'Usuario {user.username} actualizado exitosamente.')
            return redirect('users:detail', pk=user.pk)
    else:
        user_form = UserUpdateForm(instance=user)
        profile_form = UserProfileForm(instance=user.profile)
    
    context = {
        'user_obj': user,
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'users/edit.html', context)

@login_required
@superuser_required
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        username = user.username
        user.delete()
        messages.success(request, f'Usuario {username} eliminado exitosamente.')
        return redirect('users:list')
    
    return render(request, 'users/delete_confirm.html', {'user_obj': user})