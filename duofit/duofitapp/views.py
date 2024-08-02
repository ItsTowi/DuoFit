from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from duofit.settings import env
import requests
from datetime import datetime, timedelta

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
        selected_category = request.POST.get('selected_category')
        description = request.POST.get('description', '')  # Descripción opcional

        exercice_config = ExerciceConfig.objects.filter(id_user=user.id).exists()

        # Registra un nuevo entrenamiento en la fecha actual
        if exercice_config:
            new_training = ExerciceLog.objects.create(user=user, date=timezone.now())
            exercice_config_instance = ExerciceConfig.objects.get(id_user=user.id)
            exercice_config_instance.add_streak()

            # Llamar a la función de integración con la API de Notion
            notion_api_integration(new_training, selected_category, description)

        return redirect('index')  # Redirige de nuevo a la página principal

    return redirect('index')

def statistics_view(request):
    user = request.user
    exercice_config = ExerciceConfig.objects.get(id_user=user)

    # Obtener todas las fechas de entrenamiento para el usuario
    training_dates = ExerciceLog.objects.filter(
        user=user,
    ).values_list('date', flat=True)

    # Convertir las fechas a formato de cadena
    training_dates_str = [date.strftime('%Y-%m-%d') for date in training_dates]

    return render(request, 'statistics.html', {
        'streak': exercice_config.streak,
        'training_dates': training_dates_str
    })

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


def notion_api_integration(new_training, category, description):
    # Integración con la API de Notion
    database_id = '0d10e31329694a2db4a2a390713af72b'
    notion_integration_token = env('NOTION_SECRET_KEY')
    headers = {
        'Authorization': f'Bearer {notion_integration_token}',
        'Content-Type': 'application/json',
        'Notion-Version': '2022-06-28',  # Versión de la API de Notion
    }

    notion_api_url = 'https://api.notion.com/v1/pages'

    current_date_str = str(timezone.now().date())
    latest_row = read_latest_notion_row(database_id, notion_integration_token)

    if latest_row:
        training_number = latest_row['properties']['Descripción']['title'][0]['text']['content'].split()[-1]
        training_number = int(training_number) + 1
    else:
        training_number = 1

    # Datos para enviar a la API de Notion
    new_training_data = {
        'parent': {
            'database_id': database_id,
        },
        'properties': {
            'Descripción': {
                'title': [{'text': {'content': f'Training {training_number}'}}],
            },
            'Fecha': {
                'date': {'start': current_date_str},
            },
            'Categoria': {
                'select': {'name': category}
            },
            'Comentarios': {
                'rich_text': [{'text': {'content': description}}]
            }
        }
    }

    # Realizar la solicitud POST a la API de Notion
    response = requests.post(notion_api_url, headers=headers, json=new_training_data)

    # Comprobar si la solicitud fue exitosa (código de estado 200)
    if response.status_code == 200:
        # Opcionalmente, maneja la respuesta de la API de Notion
        notion_response_data = response.json()
        print("Notion API Response:", notion_response_data)
    else:
        print(response.text)


def read_latest_notion_row(database_id, notion_integration_token):
    headers = {
        'Authorization': f'Bearer {notion_integration_token}',
        'Content-Type': 'application/json',
        'Notion-Version': '2022-06-28',
    }

    notion_api_url = f'https://api.notion.com/v1/databases/{database_id}/query'

    # Configura la consulta para ordenar por fecha en orden descendente
    query_params = {
        'sorts': [{'property': 'Fecha', 'direction': 'descending'}],
    }

    # Realiza la solicitud POST a la API de Notion con los parámetros de consulta
    response = requests.post(notion_api_url, headers=headers, json=query_params)

    if response.status_code == 200:
        data = response.json()
        # Obtén la primera fila (la más nueva) si hay resultados
        if data.get('results'):
            latest_row = data['results'][0]
            return latest_row
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None
