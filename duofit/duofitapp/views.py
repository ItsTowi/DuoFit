from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

from .models import ExerciceConfig, ExerciceLog
from django.utils import timezone
from .forms import ExerciceConfigForm
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


def index(request):
    if not request.user.is_authenticated:
        return redirect('login')

    user_id = request.user.id
    exercice_config = ExerciceConfig.objects.filter(id_user=user_id).first()

    if not exercice_config:
        return redirect('settings')  # Redirige a la página de configuración si no hay configuración existente

    # Obtén el número de entrenamientos completados hoy
    today_completed_trainings = exercice_config.get_today_completed_trainings()

    return render(request, 'index.html', {'today_completed_trainings': today_completed_trainings})
    
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def signup_view(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully. You are now logged in.')
            return redirect('index')

    return render(request, 'signup.html', {'form': form})

# Create your views here.

def settings_view(request):
    if request.method == 'POST':
        form = ExerciceConfigForm(request.POST)
        if form.is_valid():
            config = form.save(commit=False)
            config.id_user = request.user  # Establece el usuario actual
            config.save()
            return redirect('index')  # Redirige a la página principal o donde desees
    else:
        form = ExerciceConfigForm()

    return render(request, 'settings.html', {'form': form})


def log_training(request):
    if request.method == 'POST':
        user = request.user
        exercice_config = ExerciceConfig.objects.filter(id_user=user.id).exists()

        # Registra un nuevo entrenamiento en la fecha actual
        if exercice_config:
            ExerciceLog.objects.create(user=user, date=timezone.now())

        return redirect('index')  # Redirige de nuevo a la página principal

    return redirect('index')



