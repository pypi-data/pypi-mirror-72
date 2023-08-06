from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(models.Environment)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(models.Entity)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name']