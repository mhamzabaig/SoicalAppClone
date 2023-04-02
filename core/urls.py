from django.urls import path
from .import views

urlpatterns = [
    path('', views.index ,name='index'),
    path('settings', views.settings ,name='settings'),
    path('follow', views.follow ,name='follow'),
    path('upload_post', views.upload_post ,name='upload_post'),
    path('like-post', views.like_post ,name='like-post'),
    path('profile/<str:pk>', views.profile ,name='profile'),
    path('signup',views.signup, name = 'signup'),
    path('signin',views.SignIn, name = 'SignIn'),
    path('logout',views.logout, name = 'logout')
]