from django.contrib import admin

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
