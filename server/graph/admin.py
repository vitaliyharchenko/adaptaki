from django.contrib import admin
from .models import Subject, Concept, Node, NodeRelation


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']


@admin.register(Concept)
class ConceptAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'is_active']
    list_filter = ['subject', 'is_active']
    search_fields = ['title']


@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):
    list_display = ['title', 'type', 'subject', 'concept', 'testability']
    list_filter = ['type', 'subject', 'concept', 'testability']
    search_fields = ['title']


@admin.register(NodeRelation)
class NodeRelationAdmin(admin.ModelAdmin):
    list_display = ['parent', 'child']
    list_filter = ['parent__subject', 'child__subject']
    search_fields = ['parent__title', 'child__title']
