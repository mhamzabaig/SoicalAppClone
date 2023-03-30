from django.urls import path
from .import views

urlpatterns = [
    path('', views.index ,name='index'),
    path('settings', views.settings ,name='settings'),
    path('signup',views.signup, name = 'signup'),
    path('signin',views.SignIn, name = 'SignIn'),
    path('logout',views.logout, name = 'logout')
]