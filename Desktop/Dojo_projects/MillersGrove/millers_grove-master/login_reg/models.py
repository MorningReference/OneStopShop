from django.db import models
import re

class RegManager(models.Manager):
    def basic_validator(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-0._-]+\.[a-zA-Z]+$')
        PASSWORD_REGEX = re.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,16})")
        errors = {}
        
        if len(postData["first_name"]) == 0:
            errors["first_name"] = "First Name must not be left blank."
        elif len(postData["first_name"]) < 2:
            errors["first_name"] = "First name must be more than 2 characters"
        elif len(postData["first_name"]) > 30:
            errors["first_name"] = "First name can not be longer than 30 characters"
        
        if len(postData["last_name"]) == 0:
            errors["last_name"] = "Last Name must not be left blank."
        elif len(postData["last_name"]) < 2:
            errors["last_name"] = "Last name must be more than 2 characters"
        elif len(postData["last_name"]) > 30:
            errors["last_name"] = "Last name can not be longer than 30 characters"
        
        user = User.objects.filter(email=postData["email"])
        if len(postData["email"]) == 0:
            errors["email"] = "Email can not be left blank."
        elif len(postData["email"]) < 6:
            errors["email"] = "Invalid email address!"
        elif not EMAIL_REGEX.match(postData["email"]):
            errors["email"] = "Invalid email address.!"
        elif user:
            errors["email"] = "Please use another email address"
        
        if len(postData["password"]) == 0:
            errors["password"] = "Password cannot be left blank."
        elif len(postData["password"]) < 8:
            errors["password"] = "Password must be a minimum of 8 characters in legnth."
        elif not PASSWORD_REGEX.match(postData["password"]):
            errors["password"] = "Password must contain 1 lowercase, 1 uppercase letter, 1 number, 1 special character-excluding !@#$%^&*"
        elif postData["password"] != postData["confirm_pw"]:
            errors["password"] = "Passwords do not match."
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=20)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = RegManager()