from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
import requests

from .models import ExerciceConfig, ExerciceLog
from django.utils import timezone
from .forms import ExerciceConfigForm
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


from datetime import datetime

def index(request):
    if not request.user.is_authenticated:
        return redirect('login')

    user_id = request.user.id
    exercice_config = ExerciceConfig.objects.filter(id_user=user_id).first()

    if not exercice_config:
        return redirect('settings')

    # Actualizar streak al abrir la página
    refresh_streak(user_id)

    return render(request, 'index.html', {
        'exercice_config': exercice_config,
        'today_completed_trainings': exercice_config.get_today_completed_trainings(),
        'today_goal': exercice_config.get_today_goal(),
        'weekly_completed_trainings': exercice_config.get_weekly_trainings(),
    })

    
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


def logout_user(request):
    logout(request)
    return redirect('index')

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


def editconfig_view(request):
    existing_config = ExerciceConfig.objects.filter(id_user=request.user).first()

    if request.method == 'POST':
        form = ExerciceConfigForm(request.POST, instance=existing_config)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ExerciceConfigForm(instance=existing_config)

    return render(request, 'edit_config.html', {'form': form})



def log_training(request):
    if request.method == 'POST':
        user = request.user
        exercice_config = ExerciceConfig.objects.filter(id_user=user.id).exists()

        # Registra un nuevo entrenamiento en la fecha actual
        if exercice_config:
            new_training = ExerciceLog.objects.create(user=user, date=timezone.now())
            exercice_config_instance = ExerciceConfig.objects.get(id_user=user.id)
            exercice_config_instance.add_streak()

            # Call the Notion API function
            #notion_api_integration(new_training)

        return redirect('index')  # Redirige de nuevo a la página principal

    return redirect('index')


#Utility functions

def refresh_streak(user_id):
    exercice_config = ExerciceConfig.objects.get(id_user=user_id)
    today_goal = exercice_config.get_today_goal()
    today_completed_trainings = exercice_config.get_today_completed_trainings()

    if today_goal <= 0 and exercice_config.streak >= 1:
        # Verificar que hoy no haya entrenamientos
        if today_completed_trainings == 0:
            exercice_config.streak += 1
            exercice_config.last_training_date = timezone.now()
            exercice_config.save()


def notion_api_integration(new_training):
    # Your Notion API integration
    notion_integration_token = 'secret_mpETsJupCH7hksg6Iq5i0IiRAhEWchet26eB36ypqmK'
    headers = {
        'Authorization': f'Bearer {notion_integration_token}',
        'Content-Type': 'application/json',
        'Notion-Version': '2022-06-28',  # Set the Notion-Version header to the latest version
    }

    notion_api_url = 'https://api.notion.com/v1/pages'

    current_date_str = str(timezone.now().date())

    # Data to be sent to Notion API to create a new row
    new_training_data = {
        'parent': {
            'database_id': '0d10e31329694a2db4a2a390713af72b',
        },
        'properties': {
            'Descripción': {
                'title': [{'text': {'content': f'Training {new_training.id}'}}],
            },
            'Fecha': {
                'date': {'start': current_date_str},
            }
        }
    }

    # Make a POST request to the Notion API
    response = requests.post(notion_api_url, headers=headers, json=new_training_data)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Optionally, handle the Notion API response
        notion_response_data = response.json()
        print("Notion API Response:", notion_response_data)
    else:
        print(response.text)
