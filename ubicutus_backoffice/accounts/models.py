from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
#from datetime import datetime
from datetime import date

# Create your models here.

class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	position = models.CharField(max_length=60, default='')

class  Task(models.Model):
	name = models.CharField(max_length=60, default='')
	description = models.TextField(max_length=1000, default='')
	date = models.DateField( default=date.today)
	progress = models.IntegerField( default=0)

class TimeInterval(models.Model):
	init_time = models.DateField()
	end_time = models.DateField()
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
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()