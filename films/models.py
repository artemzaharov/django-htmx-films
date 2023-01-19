from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.functions import Lower

class User(AbstractUser):
    pass

class Film(models.Model):
    name = models.CharField(max_length=100, unique=True)
    # through is the name of the model that will be created to manage the relationship
    users = models.ManyToManyField(User, related_name='films', through="UserFilms") #
    photo = models.ImageField(upload_to='film_photos', blank=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = [Lower('name')]  
    
class UserFilms(models.Model):
    '''This model is used to manage the relationship between User and Film with an extra field: order '''
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField()
    
    class Meta:
        ordering = ['order']



