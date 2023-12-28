from django.contrib.auth.models import User
from django.db import models



class ExerciceConfig(models.Model):
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    monday_goal = models.IntegerField()
    tuesday_goal = models.IntegerField()
    wednesday_goal = models.IntegerField()
    thursday_goal = models.IntegerField()
    friday_goal = models.IntegerField()
    saturday_goal = models.IntegerField()
    sunday_goal = models.IntegerField()
    weekly_goal = models.IntegerField()


# Create your models here.
