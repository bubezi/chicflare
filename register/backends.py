from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.backends import BaseBackend


class EmailBackend(object):
    @staticmethod
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(email=username)

        except User.MultipleObjectsReturned:
            user = User.objects.filter(email=username).order_by('id').first()
        except User.DoesNotExist:
            raise ValidationError("Invalid credentials")
            return None

        if getattr(user, 'is_active') and user.check_password(password):
            return user

    @staticmethod
    def get_user(user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None