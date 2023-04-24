from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# from store.models import Customer


# Create your models here.
class SpecialOrder(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    area = models.CharField(max_length=200, null=True)
    item = models.CharField(max_length=100, null=True)
    item_type = models.CharField(max_length=100, null=True)
    amount = models.BigIntegerField(default=0, blank=True, null=True)
    created_time = models.DateTimeField(default=timezone.now, null=True)
    processed_time = models.DateTimeField(null=True)
    completed_time = models.DateTimeField(null=True)
    processed = models.BooleanField(default=False, null=True, blank=False)
    completed = models.BooleanField(default=False, null=True, blank=False)

    def __str__(self):
        return self.item
