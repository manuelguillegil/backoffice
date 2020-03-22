from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
#from datetime import datetime
from datetime import datetime
from enum import Enum

# Create your models here.

class UserProfile(models.Model):

    REQSTUDENT = 'RS'
    PERMSTUDENT = 'PS'
    TRAINEE = 'TR'
    JUNIOR = 'JR'
    SEMISENIOR = 'SS'
    SENIOR = 'SR'

    Position = [
        (REQSTUDENT,'Estudiante por requerimientos'),
        (PERMSTUDENT,'Estudiante fijo'),
        (TRAINEE,'Trainee'),
        (JUNIOR,'Junior'),
        (SEMISENIOR,'Semi-Senior'),
        (SENIOR,'Senior'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    position = models.CharField(
        max_length=60,
        choices=Position,
        default=REQSTUDENT,
    )
    remaining_vac_days = models.IntegerField(default=30)

class  Task(models.Model):

    class Status(models.TextChoices):
        NEW = 'New'
        INPROGRESS = 'In progress'
        WAITING = 'Waiting'
        CLOSED = 'Closed'

    name = models.CharField(max_length=60, default='')
    description = models.TextField(max_length=1000, default='')
    init_date = models.DateTimeField(default=datetime.now)
    end_date = models.DateTimeField(blank=True, null=True, default=None)
    status = models.CharField(
        max_length=60,
        choices=Status.choices,
        default=Status.NEW,
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE,default=1)

class TimeInterval(models.Model):
    init_time = models.DateTimeField(default=datetime.now)
    end_time = models.DateTimeField(blank=True, null=True, default=None)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    task = models.ForeignKey(Task,on_delete=models.CASCADE)

class Vacation(models.Model):
    init_date = models.DateTimeField(blank=True, null=True, default=None)
    end_date = models.DateTimeField(blank=True, null=True, default=None)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    description = models.TextField(max_length=1000, default='')
    aproved = models.BooleanField(default=False)

class Advancement(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=30)
    description = models.TextField(max_length=1000, default='')
    aproved = models.BooleanField(default=False)

class Report(models.Model):
    date = models.DateTimeField(blank=True, null=True, default=None)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    description = models.TextField(max_length=1000, default='')


######### signals

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()