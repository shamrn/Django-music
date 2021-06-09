from django.contrib import admin
from .models import Profile,MusicalInventory,Song,Like

@admin.register(Profile)
class ______(admin.ModelAdmin):
    list_display = ['telegram']

@admin.register(MusicalInventory)
class _(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Song)
class __(admin.ModelAdmin):
    list_display = ['profile']

@admin.register(Like)
class ____(admin.ModelAdmin):
    list_display = ['song']