from django.contrib import admin
from django.contrib.auth import get_user_model

import api.models as models


@admin.register(models.GameType)
class GameTypeAdmin(admin.ModelAdmin):
    list_display = ["name"]
    list_filter = ["name"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ("name",)}
    ordering = ["name"]
    show_facets = admin.ShowFacets.ALWAYS


@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "language"]
    list_filter = ["language"]
    search_fields = ["name"]
    ordering = ["name", "language"]
    show_facets = admin.ShowFacets.ALWAYS


@admin.register(models.ContactRequest)
class ContactAdmin(admin.ModelAdmin):
    list_display = ["email", "created"]
    list_filter = ["email"]
    search_fields = ["email"]
    ordering = ["-created"]
    show_facets = admin.ShowFacets.ALWAYS


@admin.register(get_user_model())
class UserAdmin(admin.ModelAdmin):
    list_display = ["email", "first_name", "last_name", "is_active", "is_staff"]
    list_filter = ["email", "first_name"]
    search_fields = ["email", "first_name"]
    ordering = ["-date_joined"]
    show_facets = admin.ShowFacets.ALWAYS


@admin.register(models.HangmanGame)
class HangmanGameAdmin(admin.ModelAdmin):
    list_display = ["player", "status", "solution", "attempts_left"]
    list_filter = ["player", "status"]
    search_fields = ["player"]
    show_facets = admin.ShowFacets.ALWAYS
