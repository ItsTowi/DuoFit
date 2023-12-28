from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import ExerciceConfig


def index(request):

    if not request.user.is_authenticated:
        return redirect('login')
    else:
        user_id = request.user.id
        exercice_config = ExerciceConfig.objects.filter(id_user=user_id).exists()
        if exercice_config:
            return HttpResponse('Se encontro una configuración')
        else:
            return HttpResponse('No se encontró configuración')
        #Buscar si existe una configuración de ejercicio con este usuario
        #Si no existe devolver la pantalla de configuración de usuario
        #Si existe devolver la pantalla principal
        
    
def login(request):
    return HttpResponse('no logeado')

# Create your views here.
