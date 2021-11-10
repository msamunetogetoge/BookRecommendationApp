from django.urls import path

from Books import views

app_name = "Books"
urlpatterns = [
    path('', views.book_search, name='book_search'),
]