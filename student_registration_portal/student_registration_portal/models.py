from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def get_by_natural_key(self, username):
        return self.get(username=username)

class CustomUser(AbstractBaseUser):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

class Student(models.Model):
    student_name = models.CharField(max_length=100)
    registration_number = models.CharField(max_length=50)
    student_index_number = models.CharField(max_length=50)
    contact_no = models.CharField(max_length=20)
    state = models.CharField(max_length=100)
    county = models.CharField(max_length=100)
    next_of_kin = models.CharField(max_length=100)
    next_of_kin_contact = models.CharField(max_length=20)
    gender = models.CharField(max_length=10)
    admission = models.CharField(max_length=20)
    date_of_birth = models.DateField()

    def __str__(self):
        return self.student_name
