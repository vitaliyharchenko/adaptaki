from django.contrib import admin
from .models import Subject, Concept, Node, NodeRelation


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    pass


@admin.register(Concept)
class ConceptAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    search_help_text = "Поиск по названиям концептов"


@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):
    search_fields = ["title", "concept__title"]
