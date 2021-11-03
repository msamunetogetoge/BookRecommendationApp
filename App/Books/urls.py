from django.urls import path

from Books import views

urlpatterns = [
    path('', views.book_search, name='book_search'),
]