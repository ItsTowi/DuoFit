from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone



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

    def save(self, *args, **kwargs):
        self.weekly_goal = sum([getattr(self, f"{day}_goal", 0) for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]])
        super().save(*args, **kwargs)
    
    def get_today_completed_trainings(self):
        today = timezone.now().date()
        return ExerciceLog.objects.filter(user=self.id_user, date=today).count()


class ExerciceLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)


# Create your models here.
