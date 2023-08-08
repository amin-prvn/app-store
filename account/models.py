from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # TODO Maybe it is better to define default credit not in model field default
    credit = models.DecimalField(default=100, max_digits=8, decimal_places=2)