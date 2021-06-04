from django.db import models

class Profile(models.Model):
    telegram = models.CharField(max_length=150)
    first_name = models.CharField(max_length=150,null=True)
    last_name = models.CharField(max_length=150,null=True)
    instagram = models.CharField(max_length=150,null=True,blank=True)

class MusicalInventory(models.Model):
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

