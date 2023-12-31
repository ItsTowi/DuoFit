from django import forms
from .models import ExerciceConfig

class ExerciceConfigForm(forms.ModelForm):
    class Meta:
        model = ExerciceConfig
        exclude = ('id_user', 'weekly_goal', 'streak', 'last_training_date')
