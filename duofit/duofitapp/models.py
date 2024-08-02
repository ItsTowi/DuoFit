from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from datetime import datetime




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
    streak = models.IntegerField(default=0)
    last_training_date = models.DateTimeField(null=True, blank=True)
    categories = models.CharField(max_length=255, blank=True)

    def save(self, *args, **kwargs):
        self.weekly_goal = sum([getattr(self, f"{day}_goal", 0) for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]])
        super().save(*args, **kwargs)

    def get_categories(self):
        return [category.strip() for category in self.categories.split(',') if category]

    def get_today_goal(self):
        today = datetime.now().date()
        day_of_week = today.weekday()
        day_of_week_str = today.strftime('%A').lower()
        today_goal = getattr(self, f"{day_of_week_str}_goal", 0)
        return (today_goal)
    
    def get_today_completed_trainings(self):
        today = timezone.now().date()
        return ExerciceLog.objects.filter(user=self.id_user, date=today).count()
    
    def get_weekly_trainings(self):
        start_of_week = timezone.now().date() - timezone.timedelta(days=timezone.now().weekday())
        end_of_week = start_of_week + timezone.timedelta(days=6)

        return ExerciceLog.objects.filter(
            user=self.id_user,
            date__range=[start_of_week, end_of_week]
        ).count()
    
    def log_training_date(self):
        self.last_training_date = timezone.now()
        self.save()
    
    def add_streak(self):
        today_goal = self.get_today_goal()

        if today_goal > 0:
            if self.last_training_date is not None and (timezone.now() - self.last_training_date).total_seconds() > 24 * 60 * 60:
                self.streak = 0
            
            if self.get_today_completed_trainings() == today_goal:
                self.streak += 1
                self.last_training_date = timezone.now()            
                
        else:
            self.last_training_date = None

        self.save()



class ExerciceLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)


# Create your models here.
