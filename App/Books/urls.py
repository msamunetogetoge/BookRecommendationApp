from django.urls import path

from Books import views

app_name = "Books"
urlpatterns = [
    path('', views.book_search, name='book_search'),
    path('datail', views.detail, name='detail'),
    path('thoughts/<str:title>/<str:authors>/<path:thumbnail>', views.thoughts, name='thoughts'),
    path('thoughts/<str:title>/<str:authors>/', views.thoughts, name='thoughts'),
    path('thoughts/<str:title>', views.thoughts, name='thoughts'),
    path('thoughts/', views.thoughts, name='thoughts'),
    path('readend', views.readend, name='readend'),
    path('deletenotread', views.delete_not_read, name='delete_not_read'),
    
]