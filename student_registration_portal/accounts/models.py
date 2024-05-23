from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # Add any additional user fields you need, such as student ID
    student_id = models.CharField(max_length=10, unique=True)

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
