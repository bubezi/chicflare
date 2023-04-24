from django.db import models
from django.utils import timezone


class SignupLink(models.Model):
    link = models.CharField(max_length=255, unique=True)
    created_time = models.DateTimeField(default=timezone.now)
    expired_time = models.DateTimeField()
    used = models.BooleanField(default=False)


    def is_valid(self):
        now = timezone.now()
        return self.created_time <= now <= self.expired_time and not self.used
