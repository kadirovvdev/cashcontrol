from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True)
    image = models.ImageField(upload_to="user_image/", blank=True, null=True, default="user_image/default.png")

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.username

