from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


# Create your models here.
class Headline(models.Model):
    title = models.CharField(max_length=200)
    image = models.URLField(null=True, blank=True)
    url = models.TextField()

    def __str__(self):
        return self.title


class UserManager(models.Manager):
    def register_validator(self, postData):
        error = {"type": "", "data": ""}
        # Validation Rules for Email
        if len(postData['email']) < 1:
            error["type"] = "email"
            error["data"] = "Email is required"
            return error
        elif not EMAIL_REGEX.match(postData['email']):
            error["type"] = "email"
            error["data"] = "Invalid Email Address"
            return error
        if User.objects.filter(email=postData['email']):
            error["type"] = "email"
            error["data"] = "Sorry, email is already in use"
            return error

        # Validation Rules for First Name
        if len(postData['firstName']) < 1:
            error["type"] = "firstName"
            error["data"] = "First name is required"
            return error
        elif len(postData['firstName']) < 2:
            error["type"] = "firstName"
            error["data"] = "First name should be at least 2 characters"
            return error
        elif not postData['firstName'].isalpha():
            error["type"] = "firstName"
            error["data"] = "First Name can only have letters"
            return error

        # Validation Rules for Last Name
        if len(postData['lastName']) < 1:
            error["type"] = "lastName"
            error["data"] = "Last name is required"
            return error
        elif len(postData['lastName']) < 2:
            error["type"] = "lastName"
            error["data"] = "Last name should be at least 2 characters"
            return error
        elif not postData['lastName'].isalpha():
            error["type"] = "lastName"
            error["data"] = "Last name can only have letters"
            return error

        return error

    def password_validator(self, postData):
        error = {"type": "", "data": ""}
        # Validation Rules for Password
        if len(postData['password']) < 1:
            error["type"] = "password"
            error["data"] = "Password is required"
            return error
        elif len(postData['password']) < 8:
            error["type"] = "password"
            error["data"] = "Password should be at least 8 characters"
            return error

        # Validation Rules for Confirm Password
        if postData['password'] != postData['confirmPassword']:
            error["type"] = "confirmPassword"
            error["data"] = "Password and Password Confirmation did not match"
            return error

        return error

    def login_validator(self, postData):
        error = {"type": "", "data": ""}
        # Validation Rules for Login Email
        if len(postData['email']) < 1:
            error["type"] = "email"
            error["data"] = "Email is required"
            return error
        elif not EMAIL_REGEX.match(postData['email']):
            error["type"] = "email"
            error["data"] = "Invalid Email Address"
            return error
        elif not User.objects.filter(email=postData['email']):
            error["type"] = "email"
            error["data"] = "This account does not exist. Please register."
            return error

        # Validation Rules for Login Password
        if len(postData['password']) < 1:
            error["type"] = "password"
            error["data"] = "Password is required"
            return error
        else:
            user = User.objects.get(email=postData['email'])
            print(user)
            pas = user.password.encode()
            if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                error["type"] = "password"
                error["data"] = "Password is not correct"
                return error

        return error


class User(models.Model):
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return f"<User: {self.id} {self.firstName} {self.lastName} {self.email}>"

    objects = UserManager()


class RecordManager(models.Manager):
    def record_validator(self, postData):
        return ""


class Record(models.Model):
    record = models.FileField()
    user_email = models.CharField(max_length=255)
    translation = models.CharField(max_length=255)
    emotion = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return f"<Record: {self.id} {self.record} {self.user_email} {self.translation} {self.emotion}>"

    objects = RecordManager()
