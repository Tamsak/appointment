from __future__ import unicode_literals
from django.db import models
from django.core.validators import validate_email

class UserManager(models.Manager):
    def regis_validator(self, postData):
        errors = {}
        if len(postData['name']) <=0:
            errors["name"] = "Name cannot be blank"
        if len(postData['password'])<8:
            errors["password"] = "Password needs to be at least 8 characters"
        if len(postData['dob']) <=0:
            errors["dob"] = "Please choose your date of birth."
        if postData['password'] != postData['confirmed_psw']:
            errors["confirmed_psw"] = "Password doesn't match"
        try:
            validate_email(postData['email'])
        except:
            errors["email"] = "Email is not valid"
        return errors
class User(models.Model):
    name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    dob = models.DateField(max_length = 8)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()
   
class Appointment(models.Model):
    task = models.CharField(max_length =255)
    date = models.DateField(max_length=8)
    time = models.TimeField(max_length=8)
    status = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name="appointments")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()
   