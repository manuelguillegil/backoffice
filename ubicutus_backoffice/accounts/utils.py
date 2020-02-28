from enum import Enum
from django.db import models

class UserPosition(Enum):
    RS = 'Estudiante por requerimientos'
    PS = 'Estudiante fijo'
    TR = 'Trainee'
    JR = 'Junior'
    SS = 'Semi-Senior'
    SR = 'Senior'