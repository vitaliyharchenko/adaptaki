from django.contrib import admin
from .models import Concept, Node
from apps.questions.models import Question
from django.utils.safestring import mark_safe


@admin.register(Concept)
class ConceptAdmin(admin.ModelAdmin):
    search_fields = ["title__icontains"]
    search_help_text = "Поиск по названиям концептов"
    list_filter = ["subject"]


class QuestionInline(admin.TabularInline):
    model = Question.nodes.through  # доступ к промежуточной модели
    extra = 0
    verbose_name = 'Задание'
    verbose_name_plural = 'Задания'
    fields = ('question_preview', 'question_link',)
    readonly_fields = ('question_preview', 'question_link',)

    def question_link(self, instance):
        if instance.question_id:
            print(instance)
            url = f"/admin/questions/question/{instance.question_id}/change/"
            return mark_safe(f'<a href="{url}" target="_blank">Открыть задание #{instance.question_id}</a>')
        return "-"

    def question_preview(self, instance):
        if instance.question_id:
            return Question.objects.get(pk=instance.question_id)
        return "-"


@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):
    search_fields = ["title", "concept__title__icontains"]
    list_filter = ["subject", "type", "concept"]
    inlines = [QuestionInline]
