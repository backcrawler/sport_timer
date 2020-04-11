from django.contrib import admin
from .models import Exercise, Workout


@admin.register(Exercise)
class AuthorAdmin(admin.ModelAdmin):
    pass


@admin.register(Workout)
class AuthorAdmin(admin.ModelAdmin):
    pass


