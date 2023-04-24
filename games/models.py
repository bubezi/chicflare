from django.db import models
from store.models import Customer


# Create your models here.
class UserProfile(models.Model):
    player = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)


class Game(models.Model):
    game_name = models.CharField(max_length=200, null=True)

