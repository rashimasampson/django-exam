from django.db import models
import re
import bcrypt
from datetime import datetime


# Create your models here.

class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}
        # checks the email 
        email_regex = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['password']) < 8:
            errors['password'] = "Your password must be at least 8 characters"
        if len(postData['first_name']) < 2 or len(postData['last_name']) < 2:
            errors['first_name'] = "Your name must be at least 3 characters"
        if not email_regex.match(postData['email']):
            errors['email'] = 'Email must be valid'
        email_check = self.filter(email=postData['email'])
        if email_check:
            errors['email'] = "Email already in use"
        if postData['password'] != postData['confirm']:
            errors['password'] = 'Password and Confirm PW do not match'
        return errors
    def authenticate(self, postData):
        errors = {}
        check = User.objects.filter(email=postData['email'])
        if not check:
            errors['email'] = "Email has not been registered."
        else:
            if not bcrypt.checkpw(postData['password'].encode(), check[0].password.encode()):
                errors['email'] = "Email and password do not match."
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class TripManager(models.Manager):
    def trip_validate(self, postData):
        errors = {}
        if len(postData['destination']) < 1:
            errors['destination'] = 'Destination cannot be empty'
        if len(postData['description']) < 1:
            errors['description'] = 'Description cannot be empty'
        return errors

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    planner = models.ForeignKey(User, related_name='travel_creator', on_delete=models.CASCADE)
    start_date=models.DateField(null=True)
    end_date=models.DateField(null=True)
    join=models.BooleanField(default=True)
    objects = TripManager()
