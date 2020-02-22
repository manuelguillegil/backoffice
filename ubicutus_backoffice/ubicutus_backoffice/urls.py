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

urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^dashboard/$', views.index, name='home'),
    url(r'^login/$', views_account.login, name='login'),
    url(r'^signup/$', views_account.signup, name='signup'),
    url(r'^profile/$', views_account.profile, name='profile'),
    url(r'^vacaciones/$', views.vacaciones, name='vacaciones'),
    url(r'^adelanto/$', views.adelanto, name='adelanto'),
    url(r'^horas_trabajadas/$', views.consulta_horas_trabajadas, name='horas_trabajadas'),
    url(r'^registro_horas/$', views.registro_horas_trabajadas, name='registrar_horas'),
    url(r'^reporte/$', views.reporte, name='reporte_falta'),
    path('jet/', include('jet.urls', 'jet')),
    path('jet/', include('jet.urls', 'jet')),
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('admin/', admin.site.urls),
]
