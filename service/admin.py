from django.contrib import admin
from .models import Profile,MusicalInventory

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['telegram']

@admin.register(MusicalInventory)
class _(admin.ModelAdmin):
    list_display = ['name']

