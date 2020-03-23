from django.contrib import admin
from .models import Exercise, Break, Workout


@admin.register(Exercise)
class AuthorAdmin(admin.ModelAdmin):
    pass


@admin.register(Break)
class AuthorAdmin(admin.ModelAdmin):
    pass


@admin.register(Workout)
class AuthorAdmin(admin.ModelAdmin):
    pass


