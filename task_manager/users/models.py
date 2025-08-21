from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    first_name = models.CharField(
        max_length=150,
        blank=False,
        verbose_name='First Name'
    )
    last_name = models.CharField(
        max_length=150,
        blank=False,
        verbose_name='Last Name'
    )
    USERNAME_FIELD = 'username'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'