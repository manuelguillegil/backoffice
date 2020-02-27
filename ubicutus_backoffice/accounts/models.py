from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
#from datetime import datetime
from datetime import date

# Create your models here.

class UserProfile(models.Model):

    class Position(models.TextChoices):
        REQSTUDENT = 'Estudiante por requerimientos'
        PERMSTUDENT = 'Estudiante fijo'
        TRAINEE = 'Trainee'
        JUNIOR = 'Junior'
        SEMISENIOR = 'Semi-Senior'
        SENIOR = 'Senior'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    position = models.CharField(
        max_length=60,
        choices=Position.choices,
        default=Position.REQSTUDENT,
    )

class  Task(models.Model):

    class Status(models.TextChoices):
        NEW = 'New'
        INPROGRESS = 'In progress'
        WAITING = 'Waiting'
        CLOSED = 'Closed'

    name = models.CharField(max_length=60, default='')
    description = models.TextField(max_length=1000, default='')
    init_date = models.DateField(default=date.today)
    end_date = models.DateField(blank=True, null=True, default=None)
    status = models.CharField(
        max_length=60,
        choices=Status.choices,
        default=Status.NEW,
    )

class TimeInterval(models.Model):
    init_time = models.TimeField(auto_now_add=True)
    end_time = models.TimeField(auto_now=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    task = models.ForeignKey(Task,on_delete=models.CASCADE)

######### Relations

class UserTaskAssignRelation(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    task = models.ForeignKey(Task,on_delete=models.CASCADE)


######### signals

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()