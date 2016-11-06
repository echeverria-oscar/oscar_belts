from __future__ import unicode_literals
from datetime import datetime, date
from django.db import models
import bcrypt

from django.db import models

# Create your models here.
class UserManager(models.Manager):
    def login(self, post):
        user_list = User.objects.filter(username = post['username'])
        if user_list:
            user = user_list[0]
            if bcrypt.hashpw(post['password'].encode(), user.password.encode()) == user.password:

                return user
        return None

    def register(self, post):
        encrypted_password = bcrypt.hashpw(post['password'].encode(), bcrypt.gensalt())
        User.objects.create(name = post['name'], username = post['username'],date_hired = post['date_hired'], password = encrypted_password )

    def validate(self, post):
        errors = []
        today = date.today()
        print today

        if len(post['name']) == 0:
            errors.append("Name is required")
        elif len(post['name']) < 3:
            errors.append("Name is too short")

        if len(post['username']) == 0:
            errors.append("username is required")
        elif len(post['username']) < 3:
            errors.append("Username is too short")


        if len(post['password']) == 0:
            errors.append("must enter a password")
        elif len(post['password']) < 8:
            errors.append("password must have at least 8 characters")
        elif post['password'] != post['confirm_pass']:
            errors.append("password and confirmation must match")

        if not post['date_hired']:
            errors.append("Date Hired Field cannot be empty")
        try:
            date_hired = datetime.strptime(post['date_hired'], '%Y-%m-%d')
            if date_hired.date() > today:
                errors.append("Date cannot from the future")
        except:
            errors.append("Please enter a valid date for the From Date")

        return errors
class WishManager(models.Manager):
    def v_wish(self,post):
        errors = []

        if len(post['wish']) == 0:
            errors.append("Wish is required")
        elif len(post['wish']) < 3:
            errors.append("Wish is too short")
        return errors

class User(models.Model):
    name = models.CharField(max_length = 45)
    username = models.CharField(max_length = 45)
    date_hired = models.DateField()
    password = models.CharField(max_length = 100)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Wish(models.Model):
    user = models.ForeignKey(User)
    wish = models.TextField(max_length = 1000)
    wisher = models.ManyToManyField(User, related_name= "other_wish")
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = WishManager()
