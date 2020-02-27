from django.urls import path
from . import views
from django.conf.urls import url
from django.contrib.auth.views import LoginView, LogoutView



urlpatterns = [
    path('', views.indexView,name="home"),
    path('dashboard/',views.dashboardView,name="dashboard"),
    path('login/',LoginView.as_view(),name="login_url"),
    path('register/',views.registerView,name="register_url"),
    path('logout/',LogoutView.as_view(next_page='home'),name="logout"),
    
    url(r'^personal_data/$', views.user_data, name = 'user_data'),
    url(r'^personal_data/edit/$', views.edit_user_data, name = 'edit_user_data'),

]