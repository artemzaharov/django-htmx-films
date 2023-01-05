from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class Film(models.Model):
    name = models.CharField(max_length=100, unique=True)
    user = models.ManyToManyField(User, related_name='films') # user.films.all()

    def __str__(self):
        return self.name
    

