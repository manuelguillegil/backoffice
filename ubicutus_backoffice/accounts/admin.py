from django.contrib import admin
from .models import UserProfile, Task, TimeInterval, UserTaskAssignRelation

# Register your models here.
admin.site.register( UserProfile )
admin.site.register( Task )
admin.site.register( TimeInterval )
admin.site.register( UserTaskAssignRelation )