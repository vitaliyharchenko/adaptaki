from django.contrib import admin
from .models import Subject, Concept, Node, NodeRelation


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    pass


@admin.register(Concept)
class ConceptAdmin(admin.ModelAdmin):
    pass


@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):
    pass


@admin.register(NodeRelation)
class NodeRelationAdmin(admin.ModelAdmin):
    pass