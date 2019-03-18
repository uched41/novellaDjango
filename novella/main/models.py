from django.db import models
from django import forms
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
import datetime

# Create your models here.

class MyUserManager(BaseUserManager):
    def create_user(self, username, email, name, password):
        user = None

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            name=name,
        )

        #user.dateCreated = datetime.datetime.now()
        user.set_password(password)
        user.save(using=self._db)
        return user 

    def create_superuser(self, username, email, name, password):
        user = self.create_user(
            username,
            email,
            name,
            password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user 


class MyUser(AbstractBaseUser):
    username = models.CharField(
        verbose_name='username',
        max_length=40,
        unique=True,
    )
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=40)
    dateCreated = models.DateTimeField(blank=True, auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Lampbody(models.Model):
    uid = models.CharField(max_length=20, blank=True)
    settings = models.TextField(blank=True)               

    def __str__(self):
        return self.id


class Lampshade(models.Model):
    uid = models.CharField(max_length=20, blank=True)
    lampbody = models.OneToOneField(
        Lampbody,
        blank=True,
        null=True,
        on_delete=models.CASCADE
        )
    settings = models.TextField(blank=True)  

    def __str__(self):
        return self.id



class Lamp(models.Model):
    lampshade = models.OneToOneField(
        Lampshade,
        null=True,
        on_delete=models.CASCADE
        )

    brightness = models.PositiveSmallIntegerField(default=50, blank=True)
    brightnessMode = models.PositiveSmallIntegerField(default=0, blank=True)
    delayBetweenColumns = models.PositiveSmallIntegerField(default=100, blank=True)
    divider = models.PositiveSmallIntegerField(default=16, blank=True)
    currentImage = models.CharField(max_length=40, blank=True)

    motorSpeed = models.PositiveSmallIntegerField(default=50, blank=True)
    coldLedBrightness = models.PositiveSmallIntegerField(default=50, blank=True)
    warmLedBrightness = models.PositiveSmallIntegerField(default=50, blank=True)

    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

    def settings(self, mtype):
        if mtype == "lampbody":
            data = {
            "command" : "Saved_Data",
            "ColdLed_Brightness" : self.coldLedBrightness,
            "WarmLed_Brightness" : self.warmLedBrightness,
            "Motor_Speed" : self.motorSpeed,
            }

        elif mtype == "lampshade":
            data = {
            "command" : "Saved_Data",
            "Brightness" : self.brightness,
            "Brightness_Mode" : self.brightnessMode,
            "Delay_Columns" : self.delayBetweenColumns,
            "Divider": self.divider,
            "Image" : self.currentImage,
            }
        return data