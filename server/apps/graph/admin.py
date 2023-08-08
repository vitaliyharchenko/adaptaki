from django.contrib import admin
from .models import Concept, Node


@admin.register(Concept)
class ConceptAdmin(admin.ModelAdmin):
    search_fields = ["title__icontains"]
    search_help_text = "Поиск по названиям концептов"


@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):
    search_fields = ["title", "concept__title__icontains"]
    list_filter = ["subject", "type"]
