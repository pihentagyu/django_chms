from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

# Create your models here.

#class UserManager(BaseUserManager):
#    def create_user(self, email, username, display_name=None, password=None):
#        if not email:
#            raise ValueError('Users must have email address')
#        if not display_name:
#            display_name = username
#        user = self.model(
#                email = self.normalize_email(email),
#                username = username,
#                display_name = display_name
#                )
#        user.set_password(password)
#        user.save()
#        return user
#              
#
#    def create_superuser(self, email, username, display_name, password):
#        user = self.create_user(
#                email,
#                username,
#                display_name,
#                password
#                )
#        user.is_staff = True
#        user.is_superuser = True
#        #user.set_password(password)
#        user.save()
#        return user
#
#
#class User(AbstractBaseUser, PermissionsMixin):
#    email = models.EmailField(unique=True)
#    username = models.CharField(max_length=40, unique=True)
#    display_name = models.CharField(max_length=140)
#    bio = models.CharField(max_length=140, blank=True, default='')

