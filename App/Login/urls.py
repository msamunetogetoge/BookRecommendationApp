from django.urls import path

from Login import views

app_name="Login"
urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup, name='signup'),
]