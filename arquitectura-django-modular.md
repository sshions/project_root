# Arquitectura Base Modular Django - Documentación Completa

## 📋 Tabla de Contenidos

1. [Visión General](#visión-general)
2. [Estructura de Carpetas](#estructura-de-carpetas)
3. [Configuración Inicial](#configuración-inicial)
4. [Base de Datos Flexible](#base-de-datos-flexible)
5. [Sistema de Autenticación](#sistema-de-autenticación)
6. [Dashboard con Widgets](#dashboard-con-widgets)
7. [Sidebar Modular](#sidebar-modular)
8. [Gestión de Usuarios (CRUD)](#gestión-de-usuarios-crud)
9. [Control de Acceso por Roles](#control-de-acceso-por-roles)
10. [Integración Frontend](#integración-frontend)
11. [Instrucciones de Implementación](#instrucciones-de-implementación)

---

## 🎯 Visión General

Esta arquitectura proporciona una base sólida, modular y escalable para proyectos web Django. Está diseñada para permitir:

- **Reutilización**: Base común para múltiples proyectos
- **Modularidad**: Agregar nuevas funcionalidades sin modificar la estructura base
- **Escalabilidad**: Preparada para crecer con las necesidades del proyecto
- **Profesionalismo**: UI moderna y código limpio

### Stack Tecnológico

**Backend:**
- Django 5.0+
- Python 3.10+
- SQLite (desarrollo) / PostgreSQL (producción)

**Frontend:**
- HTML5
- Tailwind CSS 3.x
- Font Awesome 6.x
- Alpine.js 3.x
- Chart.js 4.x

---

## 📁 Estructura de Carpetas

```
proyecto_base/
│
├── config/                          # Configuración principal del proyecto
│   ├── __init__.py
│   ├── settings.py                  # Configuraciones generales
│   ├── settings_dev.py              # Configuraciones de desarrollo
│   ├── settings_prod.py             # Configuraciones de producción
│   ├── urls.py                      # URLs principales
│   ├── wsgi.py
│   └── asgi.py
│
├── apps/                            # Todas las aplicaciones del proyecto
│   │
│   ├── core/                        # Aplicación principal
│   │   ├── migrations/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   └── context_processors.py   # Contextos globales
│   │
│   ├── authentication/              # Sistema de autenticación
│   │   ├── migrations/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── forms.py                # Formularios de login
│   │   ├── urls.py
│   │   └── views.py
│   │
│   └── users/                       # Gestión de usuarios
│       ├── migrations/
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py
│       ├── models.py               # Modelo extendido de usuario
│       ├── forms.py                # Formularios CRUD
│       ├── urls.py
│       ├── views.py                # Vistas CRUD
│       └── permissions.py          # Decoradores personalizados
│
├── templates/                       # Plantillas HTML
│   ├── base.html                   # Template base
│   ├── base_dashboard.html         # Template para dashboard
│   │
│   ├── authentication/             # Templates de autenticación
│   │   ├── login.html
│   │   └── logout.html
│   │
│   ├── dashboard/                  # Templates del dashboard
│   │   └── index.html
│   │
│   ├── users/                      # Templates de usuarios
│   │   ├── list.html
│   │   ├── create.html
│   │   ├── edit.html
│   │   ├── detail.html
│   │   └── delete_confirm.html
│   │
│   └── components/                 # Componentes reutilizables
│       ├── sidebar.html
│       ├── navbar.html
│       ├── alerts.html
│       └── charts/
│           ├── users_chart.html
│           └── activity_chart.html
│
├── static/                          # Archivos estáticos
│   ├── css/
│   │   └── custom.css
│   ├── js/
│   │   ├── main.js
│   │   ├── charts.js
│   │   └── alpine-components.js
│   └── images/
│       └── logo.png
│
├── media/                           # Archivos subidos por usuarios
│   └── avatars/
│
├── requirements/                    # Dependencias
│   ├── base.txt
│   ├── dev.txt
│   └── prod.txt
│
├── manage.py
├── .env.example                    # Ejemplo de variables de entorno
├── .gitignore
└── README.md
```

---

## ⚙️ Configuración Inicial

### 1. Instalación de Dependencias

**requirements/base.txt**
```txt
Django==5.0.1
python-decouple==3.8
Pillow==10.2.0
django-crispy-forms==2.1
crispy-tailwind==1.0.3
```

**requirements/dev.txt**
```txt
-r base.txt
django-debug-toolbar==4.2.0
```

**requirements/prod.txt**
```txt
-r base.txt
psycopg2-binary==2.9.9
gunicorn==21.2.0
whitenoise==6.6.0
```

### 2. Configuración Principal (config/settings.py)

```python
import os
from pathlib import Path
from decouple import config

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# Security
SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-this-in-production')
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party
    'crispy_forms',
    'crispy_tailwind',
    
    # Local apps
    'apps.core',
    'apps.authentication',
    'apps.users',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.core.context_processors.global_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'America/Lima'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Authentication
LOGIN_URL = '/auth/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/auth/login/'

# Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"
CRISPY_TEMPLATE_PACK = "tailwind"

# Messages
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'error',
}
```

### 3. URLs Principales (config/urls.py)

```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('auth/', include('apps.authentication.urls')),
    path('users/', include('apps.users.urls')),
]

# Servir archivos media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

---

## 💾 Base de Datos Flexible

### Configuración Multi-Entorno

**config/settings.py (continuación)**

```python
# Database configuration
DATABASE_ENGINE = config('DATABASE_ENGINE', default='sqlite')

if DATABASE_ENGINE == 'sqlite':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
elif DATABASE_ENGINE == 'postgresql':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DB_NAME'),
            'USER': config('DB_USER'),
            'PASSWORD': config('DB_PASSWORD'),
            'HOST': config('DB_HOST', default='localhost'),
            'PORT': config('DB_PORT', default='5432'),
        }
    }
elif DATABASE_ENGINE == 'mysql':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': config('DB_NAME'),
            'USER': config('DB_USER'),
            'PASSWORD': config('DB_PASSWORD'),
            'HOST': config('DB_HOST', default='localhost'),
            'PORT': config('DB_PORT', default='3306'),
        }
    }
```

### Archivo .env.example

```env
# Django Settings
SECRET_KEY=tu-clave-secreta-super-segura
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
DATABASE_ENGINE=sqlite  # opciones: sqlite, postgresql, mysql

# PostgreSQL (solo si DATABASE_ENGINE=postgresql)
# DB_NAME=nombre_base_datos
# DB_USER=usuario
# DB_PASSWORD=contraseña
# DB_HOST=localhost
# DB_PORT=5432

# MySQL (solo si DATABASE_ENGINE=mysql)
# DB_NAME=nombre_base_datos
# DB_USER=usuario
# DB_PASSWORD=contraseña
# DB_HOST=localhost
# DB_PORT=3306
```

---

## 🔐 Sistema de Autenticación

### Formulario de Login (apps/authentication/forms.py)

```python
from django import forms
from django.contrib.auth.forms import AuthenticationForm

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition duration-200',
            'placeholder': 'Usuario o Email'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition duration-200',
            'placeholder': 'Contraseña'
        })
    )
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'w-4 h-4 text-blue-600 rounded focus:ring-blue-500'
        })
    )
```

### Vistas de Autenticación (apps/authentication/views.py)

```python
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomLoginForm

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Remember me functionality
            if not form.cleaned_data.get('remember_me'):
                request.session.set_expiry(0)
            
            messages.success(request, f'¡Bienvenido {user.username}!')
            next_url = request.GET.get('next', 'dashboard')
            return redirect(next_url)
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = CustomLoginForm()
    
    return render(request, 'authentication/login.html', {'form': form})

@login_required
def logout_view(request):
    username = request.user.username
    logout(request)
    messages.info(request, f'Hasta pronto, {username}.')
    return redirect('login')
```

### URLs de Autenticación (apps/authentication/urls.py)

```python
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
```

### Template de Login (templates/authentication/login.html)

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Iniciar Sesión</title>
    
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    
    <!-- Alpine.js -->
    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
</head>
<body class="bg-gradient-to-br from-blue-50 to-indigo-100 min-h-screen flex items-center justify-center p-4">
    
    <div class="w-full max-w-md" x-data="{ showPassword: false }">
        <!-- Card -->
        <div class="bg-white rounded-2xl shadow-2xl p-8">
            
            <!-- Logo -->
            <div class="text-center mb-8">
                <div class="inline-flex items-center justify-center w-20 h-20 bg-blue-600 rounded-full mb-4">
                    <i class="fas fa-lock text-white text-3xl"></i>
                </div>
                <h2 class="text-3xl font-bold text-gray-800">Bienvenido</h2>
                <p class="text-gray-600 mt-2">Inicia sesión en tu cuenta</p>
            </div>
            
            <!-- Messages -->
            {% if messages %}
                {% for message in messages %}
                <div class="mb-4 p-4 rounded-lg {% if message.tags == 'error' %}bg-red-100 text-red-700{% elif message.tags == 'success' %}bg-green-100 text-green-700{% else %}bg-blue-100 text-blue-700{% endif %}">
                    <i class="fas fa-info-circle mr-2"></i>
                    {{ message }}
                </div>
                {% endfor %}
            {% endif %}
            
            <!-- Form -->
            <form method="post" novalidate>
                {% csrf_token %}
                
                <!-- Username -->
                <div class="mb-4">
                    <label class="block text-gray-700 font-semibold mb-2">
                        <i class="fas fa-user mr-2"></i>Usuario
                    </label>
                    {{ form.username }}
                    {% if form.username.errors %}
                        <p class="text-red-500 text-sm mt-1">{{ form.username.errors.0 }}</p>
                    {% endif %}
                </div>
                
                <!-- Password -->
                <div class="mb-4">
                    <label class="block text-gray-700 font-semibold mb-2">
                        <i class="fas fa-lock mr-2"></i>Contraseña
                    </label>
                    <div class="relative">
                        <input 
                            :type="showPassword ? 'text' : 'password'"
                            name="password"
                            class="w-full px-4 py-3 pr-12 rounded-lg border border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition duration-200"
                            placeholder="Contraseña"
                        >
                        <button 
                            type="button"
                            @click="showPassword = !showPassword"
                            class="absolute right-4 top-1/2 transform -translate-y-1/2 text-gray-500 hover:text-gray-700"
                        >
                            <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
                        </button>
                    </div>
                    {% if form.password.errors %}
                        <p class="text-red-500 text-sm mt-1">{{ form.password.errors.0 }}</p>
                    {% endif %}
                </div>
                
                <!-- Remember Me -->
                <div class="flex items-center justify-between mb-6">
                    <label class="flex items-center">
                        {{ form.remember_me }}
                        <span class="ml-2 text-gray-700">Recordarme</span>
                    </label>
                    <a href="#" class="text-blue-600 hover:text-blue-800 text-sm font-semibold">
                        ¿Olvidaste tu contraseña?
                    </a>
                </div>
                
                <!-- Submit Button -->
                <button 
                    type="submit"
                    class="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 rounded-lg transition duration-200 transform hover:scale-105 shadow-lg"
                >
                    <i class="fas fa-sign-in-alt mr-2"></i>
                    Iniciar Sesión
                </button>
            </form>
            
            <!-- Footer -->
            <div class="mt-6 text-center text-gray-600 text-sm">
                <p>¿No tienes una cuenta? <a href="#" class="text-blue-600 hover:text-blue-800 font-semibold">Regístrate</a></p>
            </div>
        </div>
        
        <!-- Copyright -->
        <div class="text-center mt-6 text-gray-600 text-sm">
            <p>&copy; 2024 Tu Empresa. Todos los derechos reservados.</p>
        </div>
    </div>
    
</body>
</html>
```

---

## 📊 Dashboard con Widgets

### Vista del Dashboard (apps/core/views.py)

```python
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
        'total_users': total_users,
        'active_users': active_users,
        'superusers': superusers,
        'recent_users': recent_users,
        'months_data': months_data,
        'users_per_month': users_per_month,
        'latest_users': latest_users,
    }
    
    return render(request, 'dashboard/index.html', context)
```

### URLs del Core (apps/core/urls.py)

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
```

### Template Base Dashboard (templates/base_dashboard.html)

```html
<!DOCTYPE html>
<html lang="es" x-data="{ sidebarOpen: true }" x-cloak>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Dashboard{% endblock %} - Sistema</title>
    
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    
    <!-- Alpine.js -->
    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
    
    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
    
    <style>
        [x-cloak] { display: none !important; }
    </style>
    
    {% block extra_css %}{% endblock %}
</head>
<body class="bg-gray-100">
    
    <!-- Navbar -->
    <nav class="bg-white shadow-lg fixed w-full top-0 z-50">
        <div class="px-4 py-3 flex items-center justify-between">
            <!-- Toggle Sidebar -->
            <button 
                @click="sidebarOpen = !sidebarOpen"
                class="text-gray-600 hover:text-gray-900 focus:outline-none"
            >
                <i class="fas fa-bars text-xl"></i>
            </button>
            
            <!-- Logo -->
            <div class="flex items-center">
                <i class="fas fa-cube text-blue-600 text-2xl mr-3"></i>
                <span class="font-bold text-xl text-gray-800">Sistema</span>
            </div>
            
            <!-- User Menu -->
            <div x-data="{ dropdownOpen: false }" class="relative">
                <button 
                    @click="dropdownOpen = !dropdownOpen"
                    class="flex items-center space-x-3 hover:bg-gray-100 rounded-lg px-3 py-2 transition"
                >
                    <div class="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center">
                        <span class="text-white font-semibold">{{ request.user.username.0|upper }}</span>
                    </div>
                    <div class="text-left hidden md:block">
                        <p class="text-sm font-semibold text-gray-800">{{ request.user.username }}</p>
                        <p class="text-xs text-gray-500">
                            {% if request.user.is_superuser %}Administrador{% else %}Usuario{% endif %}
                        </p>
                    </div>
                    <i class="fas fa-chevron-down text-gray-600"></i>
                </button>
                
                <!-- Dropdown -->
                <div 
                    x-show="dropdownOpen"
                    @click.away="dropdownOpen = false"
                    x-transition
                    class="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-xl py-2"
                >
                    <a href="#" class="block px-4 py-2 text-gray-800 hover:bg-gray-100">
                        <i class="fas fa-user mr-2"></i>Mi Perfil
                    </a>
                    <a href="#" class="block px-4 py-2 text-gray-800 hover:bg-gray-100">
                        <i class="fas fa-cog mr-2"></i>Configuración
                    </a>
                    <hr class="my-2">
                    <a href="{% url 'logout' %}" class="block px-4 py-2 text-red-600 hover:bg-red-50">
                        <i class="fas fa-sign-out-alt mr-2"></i>Cerrar Sesión
                    </a>
                </div>
            </div>
        </div>
    </nav>
    
    <div class="flex pt-16">
        <!-- Sidebar -->
        {% include 'components/sidebar.html' %}
        
        <!-- Main Content -->
        <main 
            :class="sidebarOpen ? 'ml-64' : 'ml-0'"
            class="flex-1 p-6 transition-all duration-300"
        >
            <!-- Messages -->
            {% if messages %}
                <div class="mb-6 space-y-2">
                    {% for message in messages %}
                    <div 
                        x-data="{ show: true }"
                        x-show="show"
                        x-transition
                        class="flex items-center justify-between p-4 rounded-lg {% if message.tags == 'error' %}bg-red-100 text-red-700{% elif message.tags == 'success' %}bg-green-100 text-green-700{% elif message.tags == 'warning' %}bg-yellow-100 text-yellow-700{% else %}bg-blue-100 text-blue-700{% endif %}"
                    >
                        <div>
                            <i class="fas {% if message.tags == 'error' %}fa-exclamation-circle{% elif message.tags == 'success' %}fa-check-circle{% elif message.tags == 'warning' %}fa-exclamation-triangle{% else %}fa-info-circle{% endif %} mr-2"></i>
                            {{ message }}
                        </div>
                        <button @click="show = false" class="text-xl">&times;</button>
                    </div>
                    {% endfor %}
                </div>
            {% endif %}
            
            {% block content %}{% endblock %}
        </main>
    </div>
    
    {% block extra_js %}{% endblock %}
    
</body>
</html>
```

### Template Dashboard Index (templates/dashboard/index.html)

```html
{% extends 'base_dashboard.html' %}

{% block title %}Dashboard{% endblock %}

{% block content %}
<div class="space-y-6">
    
    <!-- Header -->
    <div class="flex items-center justify-between">
        <div>
            <h1 class="text-3xl font-bold text-gray-800">Dashboard</h1>
            <p class="text-gray-600 mt-1">Bienvenido de vuelta, {{ request.user.username }}</p>
        </div>
        <div class="text-right">
            <p class="text-sm text-gray-600">Última actualización</p>
            <p class="text-lg font-semibold text-gray-800">{{ now|date:"d/m/Y H:i" }}</p>
        </div>
    </div>
    
    <!-- Stats Cards -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        
        <!-- Total Users -->
        <div class="bg-white rounded-xl shadow-lg p-6 border-l-4 border-blue-600">
            <div class="flex items-center justify-between">
                <div>
                    <p class="text-gray-600 text-sm font-semibold">Total Usuarios</p>
                    <p class="text-3xl font-bold text-gray-800 mt-2">{{ total_users }}</p>
                </div>
                <div class="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center">
                    <i class="fas fa-users text-blue-600 text-2xl"></i>
                </div>
            </div>
            <div class="mt-4 flex items-center text-sm">
                <span class="text-green-600 font-semibold">
                    <i class="fas fa-arrow-up mr-1"></i>+{{ recent_users }}
                </span>
                <span class="text-gray-600 ml-2">últimos 30 días</span>
            </div>
        </div>
        
        <!-- Active Users -->
        <div class="bg-white rounded-xl shadow-lg p-6 border-l-4 border-green-600">
            <div class="flex items-center justify-between">
                <div>
                    <p class="text-gray-600 text-sm font-semibold">Usuarios Activos</p>
                    <p class="text-3xl font-bold text-gray-800 mt-2">{{ active_users }}</p>
                </div>
                <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center">
                    <i class="fas fa-user-check text-green-600 text-2xl"></i>
                </div>
            </div>
            <div class="mt-4 flex items-center text-sm">
                <span class="text-gray-600">
                    {{ active_users|floatformat:0 }} de {{ total_users }} activos
                </span>
            </div>
        </div>
        
        <!-- Superusers -->
        <div class="bg-white rounded-xl shadow-lg p-6 border-l-4 border-purple-600">
            <div class="flex items-center justify-between">
                <div>
                    <p class="text-gray-600 text-sm font-semibold">Administradores</p>
                    <p class="text-3xl font-bold text-gray-800 mt-2">{{ superusers }}</p>
                </div>
                <div class="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center">
                    <i class="fas fa-user-shield text-purple-600 text-2xl"></i>
                </div>
            </div>
            <div class="mt-4 flex items-center text-sm">
                <span class="text-gray-600">Con acceso total</span>
            </div>
        </div>
        
        <!-- Recent Registrations -->
        <div class="bg-white rounded-xl shadow-lg p-6 border-l-4 border-orange-600">
            <div class="flex items-center justify-between">
                <div>
                    <p class="text-gray-600 text-sm font-semibold">Nuevos Registros</p>
                    <p class="text-3xl font-bold text-gray-800 mt-2">{{ recent_users }}</p>
                </div>
                <div class="w-16 h-16 bg-orange-100 rounded-full flex items-center justify-center">
                    <i class="fas fa-user-plus text-orange-600 text-2xl"></i>
                </div>
            </div>
            <div class="mt-4 flex items-center text-sm">
                <span class="text-gray-600">Últimos 30 días</span>
            </div>
        </div>
        
    </div>
    
    <!-- Charts -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        <!-- Users Chart -->
        <div class="bg-white rounded-xl shadow-lg p-6">
            <h3 class="text-xl font-bold text-gray-800 mb-4">
                <i class="fas fa-chart-line text-blue-600 mr-2"></i>
                Registros por Mes
            </h3>
            <canvas id="usersChart" height="250"></canvas>
        </div>
        
        <!-- User Status Pie Chart -->
        <div class="bg-white rounded-xl shadow-lg p-6">
            <h3 class="text-xl font-bold text-gray-800 mb-4">
                <i class="fas fa-chart-pie text-green-600 mr-2"></i>
                Estado de Usuarios
            </h3>
            <canvas id="statusChart" height="250"></canvas>
        </div>
        
    </div>
    
    <!-- Latest Users Table -->
    <div class="bg-white rounded-xl shadow-lg p-6">
        <div class="flex items-center justify-between mb-6">
            <h3 class="text-xl font-bold text-gray-800">
                <i class="fas fa-clock text-blue-600 mr-2"></i>
                Últimos Usuarios Registrados
            </h3>
            <a href="{% url 'users:list' %}" class="text-blue-600 hover:text-blue-800 font-semibold">
                Ver todos <i class="fas fa-arrow-right ml-1"></i>
            </a>
        </div>
        
        <div class="overflow-x-auto">
            <table class="w-full">
                <thead>
                    <tr class="border-b-2 border-gray-200">
                        <th class="px-4 py-3 text-left text-gray-600 font-semibold">Usuario</th>
                        <th class="px-4 py-3 text-left text-gray-600 font-semibold">Email</th>
                        <th class="px-4 py-3 text-left text-gray-600 font-semibold">Fecha Registro</th>
                        <th class="px-4 py-3 text-left text-gray-600 font-semibold">Estado</th>
                        <th class="px-4 py-3 text-left text-gray-600 font-semibold">Rol</th>
                    </tr>
                </thead>
                <tbody>
                    {% for user in latest_users %}
                    <tr class="border-b border-gray-100 hover:bg-gray-50">
                        <td class="px-4 py-3">
                            <div class="flex items-center">
                                <div class="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center mr-3">
                                    <span class="text-white font-semibold">{{ user.username.0|upper }}</span>
                                </div>
                                <span class="font-semibold text-gray-800">{{ user.username }}</span>
                            </div>
                        </td>
                        <td class="px-4 py-3 text-gray-600">{{ user.email }}</td>
                        <td class="px-4 py-3 text-gray-600">{{ user.date_joined|date:"d/m/Y" }}</td>
                        <td class="px-4 py-3">
                            {% if user.is_active %}
                            <span class="px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm font-semibold">
                                <i class="fas fa-check-circle mr-1"></i>Activo
                            </span>
                            {% else %}
                            <span class="px-3 py-1 bg-red-100 text-red-700 rounded-full text-sm font-semibold">
                                <i class="fas fa-times-circle mr-1"></i>Inactivo
                            </span>
                            {% endif %}
                        </td>
                        <td class="px-4 py-3">
                            {% if user.is_superuser %}
                            <span class="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-sm font-semibold">
                                <i class="fas fa-crown mr-1"></i>Admin
                            </span>
                            {% else %}
                            <span class="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm font-semibold">
                                <i class="fas fa-user mr-1"></i>Usuario
                            </span>
                            {% endif %}
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
    
</div>
{% endblock %}

{% block extra_js %}
<script>
    // Users per Month Chart
    const usersCtx = document.getElementById('usersChart').getContext('2d');
    new Chart(usersCtx, {
        type: 'line',
        data: {
            labels: {{ months_data|safe }},
            datasets: [{
                label: 'Registros',
                data: {{ users_per_month|safe }},
                borderColor: 'rgb(59, 130, 246)',
                backgroundColor: 'rgba(59, 130, 246, 0.1)',
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1
                    }
                }
            }
        }
    });
    
    // User Status Pie Chart
    const statusCtx = document.getElementById('statusChart').getContext('2d');
    new Chart(statusCtx, {
        type: 'doughnut',
        data: {
            labels: ['Activos', 'Inactivos', 'Administradores'],
            datasets: [{
                data: [{{ active_users }}, {{ total_users|add:"-"|add:active_users }}, {{ superusers }}],
                backgroundColor: [
                    'rgb(34, 197, 94)',
                    'rgb(239, 68, 68)',
                    'rgb(168, 85, 247)'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
</script>
{% endblock %}
```

---

## 🎨 Sidebar Modular

### Componente Sidebar (templates/components/sidebar.html)

```html
<aside 
    x-show="sidebarOpen"
    x-transition:enter="transition ease-out duration-300"
    x-transition:enter-start="-translate-x-full"
    x-transition:enter-end="translate-x-0"
    x-transition:leave="transition ease-in duration-300"
    x-transition:leave-start="translate-x-0"
    x-transition:leave-end="-translate-x-full"
    class="fixed left-0 top-16 h-full w-64 bg-white shadow-xl overflow-y-auto z-40"
>
    <nav class="p-4">
        
        <!-- Dashboard -->
        <a href="{% url 'dashboard' %}" 
           class="flex items-center px-4 py-3 mb-2 rounded-lg {% if request.resolver_match.url_name == 'dashboard' %}bg-blue-600 text-white{% else %}text-gray-700 hover:bg-gray-100{% endif %} transition">
            <i class="fas fa-home mr-3 text-lg"></i>
            <span class="font-semibold">Dashboard</span>
        </a>
        
        <!-- Users Module -->
        {% if request.user.is_superuser %}
        <div x-data="{ open: {{ 'true' if 'users' in request.path else 'false' }} }" class="mb-2">
            <button 
                @click="open = !open"
                class="w-full flex items-center justify-between px-4 py-3 rounded-lg text-gray-700 hover:bg-gray-100 transition"
            >
                <div class="flex items-center">
                    <i class="fas fa-users mr-3 text-lg"></i>
                    <span class="font-semibold">Gestión de Usuarios</span>
                </div>
                <i :class="open ? 'fa-chevron-up' : 'fa-chevron-down'" class="fas text-sm"></i>
            </button>
            
            <div x-show="open" x-transition class="ml-4 mt-2 space-y-1">
                <a href="{% url 'users:list' %}" 
                   class="flex items-center px-4 py-2 rounded-lg {% if request.resolver_match.url_name == 'list' %}bg-blue-100 text-blue-700{% else %}text-gray-600 hover:bg-gray-50{% endif %} transition">
                    <i class="fas fa-list mr-3"></i>
                    <span>Lista de Usuarios</span>
                </a>
                <a href="{% url 'users:create' %}" 
                   class="flex items-center px-4 py-2 rounded-lg {% if request.resolver_match.url_name == 'create' %}bg-blue-100 text-blue-700{% else %}text-gray-600 hover:bg-gray-50{% endif %} transition">
                    <i class="fas fa-user-plus mr-3"></i>
                    <span>Nuevo Usuario</span>
                </a>
            </div>
        </div>
        {% endif %}
        
        <!-- Divider -->
        <hr class="my-4 border-gray-200">
        
        <!-- Future Modules Placeholder -->
        <div class="px-4 py-3 text-gray-400 text-sm font-semibold uppercase">
            Módulos Futuros
        </div>
        
        <div class="space-y-2 opacity-50">
            <div class="flex items-center px-4 py-3 text-gray-400">
                <i class="fas fa-box mr-3 text-lg"></i>
                <span>Inventario</span>
            </div>
            <div class="flex items-center px-4 py-3 text-gray-400">
                <i class="fas fa-chart-bar mr-3 text-lg"></i>
                <span>Reportes</span>
            </div>
            <div class="flex items-center px-4 py-3 text-gray-400">
                <i class="fas fa-cog mr-3 text-lg"></i>
                <span>Configuración</span>
            </div>
        </div>
        
        <!-- Footer -->
        <div class="absolute bottom-0 left-0 right-0 p-4 bg-gray-50">
            <div class="text-center text-xs text-gray-500">
                <p>v1.0.0</p>
                <p class="mt-1">&copy; 2024 Tu Empresa</p>
            </div>
        </div>
        
    </nav>
</aside>
```

---

## 👥 Gestión de Usuarios (CRUD)

### Modelo de Usuario Extendido (apps/users/models.py)

```python
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'Perfil de {self.user.username}'
    
    class Meta:
        verbose_name = 'Perfil de Usuario'
        verbose_name_plural = 'Perfiles de Usuarios'

# Signal para crear perfil automáticamente
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
```

### Formularios CRUD (apps/users/forms.py)

```python
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

class UserCreateForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
        })
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
        })
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            })

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            })

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone', 'address', 'avatar', 'bio')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            })
```

### Decorador de Permisos (apps/users/permissions.py)

```python
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def superuser_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Debes iniciar sesión.')
            return redirect('login')
        
        if not request.user.is_superuser:
            messages.error(request, 'No tienes permisos para acceder a esta sección.')
            return redirect('dashboard')
        
        return view_func(request, *args, **kwargs)
    return wrapper
```

### Vistas CRUD (apps/users/views.py)

```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from .forms import UserCreateForm, UserUpdateForm, UserProfileForm
from .permissions import superuser_required

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
```

### URLs de Usuarios (apps/users/urls.py)

```python
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.user_list, name='list'),
    path('create/', views.user_create, name='create'),
    path('<int:pk>/', views.user_detail, name='detail'),
    path('<int:pk>/edit/', views.user_update, name='edit'),
    path('<int:pk>/delete/', views.user_delete, name='delete'),
]
```

### Template Lista de Usuarios (templates/users/list.html)

```html
{% extends 'base_dashboard.html' %}

{% block title %}Gestión de Usuarios{% endblock %}

{% block content %}
<div class="space-y-6">
    
    <!-- Header -->
    <div class="flex items-center justify-between">
        <div>
            <h1 class="text-3xl font-bold text-gray-800">Gestión de Usuarios</h1>
            <p class="text-gray-600 mt-1">Administra todos los usuarios del sistema</p>
        </div>
        <a href="{% url 'users:create' %}" 
           class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-lg transition shadow-lg">
            <i class="fas fa-user-plus mr-2"></i>Nuevo Usuario
        </a>
    </div>
    
    <!-- Search Bar -->
    <div class="bg-white rounded-xl shadow-lg p-6">
        <form method="get" class="flex gap-4">
            <div class="flex-1">
                <input 
                    type="text" 
                    name="q" 
                    value="{{ query }}"
                    placeholder="Buscar por usuario, email o nombre..."
                    class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
            </div>
            <button 
                type="submit"
                class="bg-blue-600 hover:bg-blue-700 text-white font-bold px-8 py-3 rounded-lg transition"
            >
                <i class="fas fa-search mr-2"></i>Buscar
            </button>
        </form>
    </div>
    
    <!-- Users Table -->
    <div class="bg-white rounded-xl shadow-lg overflow-hidden">
        <div class="overflow-x-auto">
            <table class="w-full">
                <thead class="bg-gray-50">
                    <tr>
                        <th class="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                            Usuario
                        </th>
                        <th class="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                            Email
                        </th>
                        <th class="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                            Fecha Registro
                        </th>
                        <th class="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                            Estado
                        </th>
                        <th class="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                            Rol
                        </th>
                        <th class="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                            Acciones
                        </th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-gray-200">
                    {% for user in users %}
                    <tr class="hover:bg-gray-50 transition">
                        <td class="px-6 py-4 whitespace-nowrap">
                            <div class="flex items-center">
                                <div class="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center mr-3">
                                    <span class="text-white font-semibold">{{ user.username.0|upper }}</span>
                                </div>
                                <div>
                                    <div class="font-semibold text-gray-800">{{ user.username }}</div>
                                    <div class="text-sm text-gray-600">{{ user.get_full_name }}</div>
                                </div>
                            </div>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap text-gray-600">
                            {{ user.email }}
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap text-gray-600">
                            {{ user.date_joined|date:"d/m/Y" }}
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            {% if user.is_active %}
                            <span class="px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm font-semibold">
                                <i class="fas fa-check-circle mr-1"></i>Activo
                            </span>
                            {% else %}
                            <span class="px-3 py-1 bg-red-100 text-red-700 rounded-full text-sm font-semibold">
                                <i class="fas fa-times-circle mr-1"></i>Inactivo
                            </span>
                            {% endif %}
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            {% if user.is_superuser %}
                            <span class="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-sm font-semibold">
                                <i class="fas fa-crown mr-1"></i>Admin
                            </span>
                            {% elif user.is_staff %}
                            <span class="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm font-semibold">
                                <i class="fas fa-user-tie mr-1"></i>Staff
                            </span>
                            {% else %}
                            <span class="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm font-semibold">
                                <i class="fas fa-user mr-1"></i>Usuario
                            </span>
                            {% endif %}
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            <div class="flex space-x-2">
                                <a href="{% url 'users:detail' user.pk %}" 
                                   class="text-blue-600 hover:text-blue-800" title="Ver detalles">
                                    <i class="fas fa-eye"></i>
                                </a>
                                <a href="{% url 'users:edit' user.pk %}" 
                                   class="text-green-600 hover:text-green-800" title="Editar">
                                    <i class="fas fa-edit"></i>
                                </a>
                                <a href="{% url 'users:delete' user.pk %}" 
                                   class="text-red-600 hover:text-red-800" title="Eliminar">
                                    <i class="fas fa-trash"></i>
                                </a>
                            </div>
                        </td>
                    </tr>
                    {% empty %}
                    <tr>
                        <td colspan="6" class="px-6 py-12 text-center text-gray-500">
                            <i class="fas fa-users text-4xl mb-4"></i>
                            <p>No se encontraron usuarios</p>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
    
</div>
{% endblock %}
```

---

## 🔒 Control de Acceso por Roles

### Flujo de Autenticación

```
┌─────────────────┐
│  Usuario accede │
│  a la URL       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ ¿Autenticado?   │
└────────┬────────┘
         │
    ┌────┴────┐
   NO│       │SÍ
    │         │
    ▼         ▼
┌────────┐  ┌──────────────┐
│ Login  │  │ ¿Superuser?  │
└────────┘  └──────┬───────┘
                   │
              ┌────┴────┐
             NO│       │SÍ
              │         │
              ▼         ▼
        ┌──────────┐  ┌───────────┐
        │ Dashboard│  │  Acceso   │
        │ Limitado │  │  Completo │
        └──────────┘  └───────────┘
```

### Contexto Global (apps/core/context_processors.py)

```python
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
```

### Middleware Personalizado (opcional)

```python
# apps/core/middleware.py
from django.shortcuts import redirect
from django.urls import reverse

class RoleBasedAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # URLs que requieren superuser
        superuser_urls = ['/users/']
        
        if request.user.is_authenticated:
            for url in superuser_urls:
                if request.path.startswith(url) and not request.user.is_superuser:
                    return redirect('dashboard')
        
        response = self.get_response(request)
        return response
```

---

## 🎨 Integración Frontend

### CDNs y Versiones

**Tailwind CSS**
```html
<script src="https://cdn.tailwindcss.com"></script>
```

**Font Awesome 6.5.1**
```html
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
```

**Alpine.js 3.x**
```html
<script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
```

**Chart.js 4.4.1**
```html
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
```

### CSS Personalizado (static/css/custom.css)

```css
/* Animaciones personalizadas */
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.fade-in {
    animation: fadeIn 0.3s ease-in;
}

/* Scrollbar personalizado */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
    background: #888;
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: #555;
}

/* Estilos para Alpine.js */
[x-cloak] {
    display: none !important;
}
```

### JavaScript Principal (static/js/main.js)

```javascript
// Confirmación de eliminación
function confirmDelete(message) {
    return confirm(message || '¿Estás seguro de que deseas eliminar este elemento?');
}

// Auto-hide alerts
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('[data-alert]');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });
});

// Tooltips
function initTooltips() {
    const tooltips = document.querySelectorAll('[data-tooltip]');
    tooltips.forEach(el => {
        el.addEventListener('mouseenter', function() {
            const text = this.getAttribute('data-tooltip');
            const tooltip = document.createElement('div');
            tooltip.className = 'tooltip';
            tooltip.textContent = text;
            document.body.appendChild(tooltip);
            
            const rect = this.getBoundingClientRect();
            tooltip.style.top = (rect.top - tooltip.offsetHeight - 5) + 'px';
            tooltip.style.left = (rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2)) + 'px';
        });
        
        el.addEventListener('mouseleave', function() {
            const tooltip = document.querySelector('.tooltip');
            if (tooltip) tooltip.remove();
        });
    });
}

document.addEventListener('DOMContentLoaded', initTooltips);
```

---

## 🚀 Instrucciones de Implementación

### Paso 1: Configuración del Entorno

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Instalar dependencias
pip install -r requirements/dev.txt
```

### Paso 2: Configuración del Proyecto

```bash
# Crear archivo .env
cp .env.example .env

# Editar .env con tus configuraciones
# SECRET_KEY, DEBUG, DATABASE_ENGINE, etc.
```

### Paso 3: Configuración de Base de Datos

```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser
```

### Paso 4: Recolectar Archivos Estáticos

```bash
python manage.py collectstatic --noinput
```

### Paso 5: Ejecutar Servidor de Desarrollo

```bash
python manage.py runserver
```

### Paso 6: Acceder al Sistema

```
Login: http://localhost:8000/auth/login/
Dashboard: http://localhost:8000/dashboard/
Admin: http://localhost:8000/admin/
```

---

## 📝 Checklist de Implementación

- [ ] Crear estructura de carpetas
- [ ] Configurar settings.py
- [ ] Configurar base de datos
- [ ] Crear archivo .env
- [ ] Instalar dependencias
- [ ] Crear aplicaciones (core, authentication, users)
- [ ] Configurar URLs
- [ ] Crear modelos
- [ ] Crear formularios
- [ ] Crear vistas
- [ ] Crear templates base
- [ ] Crear templates de autenticación
- [ ] Crear templates del dashboard
- [ ] Crear templates de usuarios
- [ ] Crear componente sidebar
- [ ] Integrar CDNs frontend
- [ ] Configurar archivos estáticos
- [ ] Aplicar migraciones
- [ ] Crear superusuario
- [ ] Probar login/logout
- [ ] Probar CRUD de usuarios
- [ ] Probar dashboard y widgets
- [ ] Verificar permisos por rol

---

## 🔧 Personalización para Nuevos Proyectos

### Agregar Nuevos Módulos

1. **Crear nueva app:**
```bash
python manage.py startapp nombre_modulo
```

2. **Agregar a INSTALLED_APPS** en settings.py

3. **Crear models, views, urls, templates**

4. **Agregar al sidebar** en `templates/components/sidebar.html`

### Cambiar Base de Datos

Editar `.env`:
```env
DATABASE_ENGINE=postgresql
DB_NAME=mi_base_datos
DB_USER=usuario
DB_PASSWORD=contraseña
DB_HOST=localhost
DB_PORT=5432
```

### Personalizar Colores y Estilos

Modificar `static/css/custom.css` o usar configuración de Tailwind

---

## 📚 Recursos Adicionales

### Documentación Oficial

- **Django:** https://docs.djangoproject.com/
- **Tailwind CSS:** https://tailwindcss.com/docs
- **Alpine.js:** https://alpinejs.dev/
- **Chart.js:** https://www.chartjs.org/docs/
- **Font Awesome:** https://fontawesome.com/docs

### Comandos Útiles Django

```bash
# Crear nueva migración
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Shell interactivo
python manage.py shell

# Ejecutar tests
python manage.py test

# Limpiar base de datos
python manage.py flush
```

---

## 🎯 Conclusión

Esta arquitectura proporciona una base sólida y modular para desarrollar proyectos web con Django. Los componentes están diseñados para ser:

- **Reutilizables**: Puedes usar esta base en múltiples proyectos
- **Escalables**: Fácil de extender con nuevas funcionalidades
- **Mantenibles**: Código limpio y bien organizado
- **Profesionales**: UI moderna y experiencia de usuario optimizada

### Próximos Pasos

1. Implementar sistema de recuperación de contraseña
2. Agregar perfiles de usuario más detallados
3. Implementar sistema de notificaciones
4. Agregar logs de actividad
5. Implementar API REST con Django REST Framework
6. Agregar tests unitarios y de integración
7. Configurar CI/CD para despliegue automático

---

**Autor:** Documentación Técnica  
**Versión:** 1.0.0  
**Fecha:** 2025  
**Licencia:** MIT
