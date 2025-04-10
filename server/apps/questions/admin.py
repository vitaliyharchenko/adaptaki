from django.contrib import admin
from django.forms import ModelForm
from markdownx.widgets import AdminMarkdownxWidget
from markdownx.models import MarkdownxField
from ckeditor.widgets import CKEditorWidget
from .models import Question, QuestionOption
from apps.graph.models import Concept, Node
from django.urls import reverse


class SmallMarkdownTextArea(AdminMarkdownxWidget):
    template_name = 'markdownx/widget_small.html'


class QuestionOptionInline(admin.TabularInline):
    model = QuestionOption
    fk_name = "question"
    extra = 0
    formfield_overrides = {
        MarkdownxField: {'widget': SmallMarkdownTextArea(attrs={"rows": 4, "style": 'width: 90%'})},
    }


# Создаём кастомный SimpleListFilter по Concept
class ConceptFilter(admin.SimpleListFilter):
    title = 'Концепт'
    parameter_name = 'concept'

    def lookups(self, request, model_admin):
        concepts = Concept.objects.all()
        return [(concept.id, concept.title) for concept in concepts]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(nodes__concept_id=self.value()).distinct()
        return queryset


# Создаём кастомный SimpleListFilter по Node
class NodeFilter(admin.SimpleListFilter):
    title = 'Вершина графа'
    parameter_name = 'node'

    def lookups(self, request, model_admin):
        nodes = Node.objects.all()
        return [(node.id, node.title) for node in nodes]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(nodes__id=self.value()).distinct()
        return queryset


class QuestionAdminForm(ModelForm):
    class Meta:
        model = Question
        fields = "__all__"
        widgets = {
            "question_text_new": CKEditorWidget(),
            "explanation_text_new": CKEditorWidget(),
        }


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [QuestionOptionInline]
    form = QuestionAdminForm
    list_filter = ["type", "max_score", "exam_tag", ConceptFilter, NodeFilter]
    autocomplete_fields = ["exam_tag", "nodes"]
    search_fields = ["pk", "question_text__icontains"]
    search_help_text = "Поиск по id и условию задачи"
    fieldsets = [
        ("Тип задачи", {"fields": [
            "type", "max_score", "checking_policy"]}),
        ("Условие задачи", {"fields": ["question_text_new"]}),
        ("Пояснение", {"fields": [
            "explanation_text_new", "thumbnail"]}),
        ("Привязка к рубрикаторам", {"fields": [
            "nodes", "exam_tag"], "classes": ["collapse"]}),
    ]

    def get_view_on_site_url(self, obj):
        return reverse('question_html', kwargs={'pk': obj.pk})
