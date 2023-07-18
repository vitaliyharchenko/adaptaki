from django.contrib import admin
from django.db import models
from django.forms import ModelForm
from markdownx.widgets import AdminMarkdownxWidget
from markdownx.admin import MarkdownxModelAdmin
from .models import Question, QuestionOption


class QuestionOptionInline(admin.TabularInline):
    model = QuestionOption
    fk_name = "question"
    extra = 0


class Textarea(AdminMarkdownxWidget):
    template_name = 'markdownx/widget1.html'


class QuestionAdminForm(ModelForm):
    class Meta:
        model = Question
        fields = "__all__"
        widgets = {
            "question_text": Textarea(attrs={"cols": 10, "rows": 10, "style": 'width: 95%'}),
            "explanation_text": Textarea(attrs={"cols": 10, "rows": 10}),
        }


@admin.register(Question)
class QuestionAdmin(MarkdownxModelAdmin):
    inlines = [QuestionOptionInline]
    form = QuestionAdminForm
    list_filter = ["type"]
    fieldsets = [
        ("Тип задачи", {"fields": [
            "type", "max_score", "checking_policy"]}),
        ("Условие задачи", {"fields": ["question_text", "image"]}),
        ("Пояснение", {"fields": [
            "explanation_text", "explanation_image"]}),
        ("Привязка", {"fields": [
            "nodes", "exam_tag"], "classes": ["collapse"]}),
    ]

    class Media:
        js = (
            '//cdn.jsdelivr.net/npm/mathjax@2/MathJax.js',  # mathjax
            'mathjax.js'
        )
