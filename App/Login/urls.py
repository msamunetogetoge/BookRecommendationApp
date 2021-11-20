from django.urls import path

from Login import views

app_name="Login"
urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('logout', views.logout_user, name="logout"),
    path('config', views.user_config, name='config'),
    path('register', views.register_attr, name='register_attr'),
    path('delete', views.delete_attr, name='delete_attr'),
]