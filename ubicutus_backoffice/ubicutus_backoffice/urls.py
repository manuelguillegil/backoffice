"""ubicutus_backoffice URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from main import views
from accounts import views as views_account
from django.contrib.auth.views import LoginView, LogoutView

# PURGAR URLS PLSSSSSSSSS
urlpatterns = [
    url(r'^$', views.dashboard, name='home'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^profile/$', views_account.profile, name='profile'),
    url(r'^vacaciones/$', views.vacaciones, name='vacaciones'),
    url(r'^adelanto/$', views.adelanto, name='adelanto'),
    url(r'^horas_trabajadas/$', views.consulta_horas_trabajadas, name='horas_trabajadas'),
    url(r'^registrar_tareas/$', views.registrar_tareas_trabajadas, name='registrar_tarea'),
    url(r'^registrar_hora/$', views.lista_tarea, name='lista_tareas'),
    url(r'^registrar_nueva_hora/(?P<pk>\d+)/$', views.registrar_nueva_hora, name='nueva_hora'),
    url(r'^editar_tarea/(?P<pk>\d+)/$', views.editar_tarea, name='editar_tarea'),
    url(r'^contador/', views.contador, name="contador"),
    url(r'^reporte/$', views.reporte, name='reporte_falta'),
    url(r'^tareas/$', views.tareas, name='tareas'),
    url(r'^eliminar_tarea/$', views.eliminar_tarea, name='eliminar_tarea'),
    url(r'^archivar_tarea/$', views.archivar_tarea, name='archivar_tarea'),
    url(r'^desarchivar_tarea/$', views.desarchivar_tarea, name='desarchivar_tarea'),
    url(r'^nueva_tarea/$', views.registrar_tareas_trabajadas_render, name='nueva_tarea'),


    url(r'^horas_trabajadas_admin/$', views.horas_trabajadas_admin, name='horas_trabajadas_admin'),

    path('accounts/',include('accounts.urls')),
   
    path('jet/', include('jet.urls', 'jet')),
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
   
    path('admin/', admin.site.urls),

    # Views para pasarle la informacion a los graficos
    path('status-chart/', views.status_chart, name='status-chart'),
    path('task-hours-chart/', views.task_hours_chart, name='task-hours-chart'),
    path('hours-worked-chart/', views.hours_worked_chart, name='hours-worked-chart'),

    path('clock-view/', views.clock_view , name='clock-view'),

    url(r'^edit_task/$', views.editar_tarea_new, name='editar_tarea_new'),
    url(r'^tareas_archivadas/$', views.tareas_archivadas, name='tareas_archivadas'),
    url(r'^get_task/$', views.obtener_valores, name='get_task')

]
