from django.urls import path
from . import views
from django.conf.urls import url
from django.contrib.auth.views import LoginView, LogoutView



urlpatterns = [
    path('login/',LoginView.as_view(),name="login"),
    path('register/',views.registerView,name="signup"),
    path('logout/',LogoutView.as_view(next_page='login'),name="logout"),
    
    url(r'^personal_data/$', views.user_data, name = 'user_data'),
    url(r'^personal_data/edit/$', views.edit_user_data, name = 'edit_user_data'),
]