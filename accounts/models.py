from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):

    mobile = models.CharField(max_length=20, unique=True)

    class Meta:
        db_table = "accounts.auth_user"

    def __str__(self):
        return self.username