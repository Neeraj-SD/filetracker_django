from asyncio.unix_events import BaseChildWatcher
import email
from pyexpat import model
from unicodedata import name
from django.db import models

# Create your models here.


class Batch(models.Model):
    name = models.CharField(max_length=255)


class Department(models.Model):
    name = models.CharField(max_length=255)


class Role(models.Model):
    name = models.CharField(max_length=255)


class Student(models.Model):
    first_name = models.CharField(min_length=3, max_length=255)
    last_name = models.CharField(min_length=3, max_length=255)
    email = models.EmailField()
    department = models.OneToOneField(Department, on_delete=models.SET_NULL)
    phone_number = models.CharField(max_length=255)
    batch = models.OneToOneField(Batch, on_delete=models.SET_NULL)
    admission_number = models.CharField(max_length=255)
    register_number = models.CharField(max_length=255)


class Faculty(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    department = models.OneToOneField(Department, on_delete=models.SET_NULL)
    phone_number = models.CharField(max_length=255)
    role = models.OneToOneField(Role, on_delete=models.SET_NULL)
