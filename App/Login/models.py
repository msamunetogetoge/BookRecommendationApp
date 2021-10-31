from django.db import models

# Create your models here.
class User(models.Model):
    id = models.TextField(primary_key=True)
    name = models.TextField()
    password = models.TextField()
    email= models.EmailField()
