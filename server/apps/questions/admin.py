from django.contrib import admin
from django.db import models
from django.forms import ModelForm
from markdownx.widgets import AdminMarkdownxWidget
from markdownx.admin import MarkdownxModelAdmin
from markdownx.models import MarkdownxField
from .models import Question, QuestionOption


class SmallMarkdownTextArea(AdminMarkdownxWidget):
    template_name = 'markdownx/widget_small.html'


class QuestionOptionInline(admin.TabularInline):
    model = QuestionOption
    fk_name = "question"
    extra = 0
    formfield_overrides = {
        MarkdownxField: {'widget': SmallMarkdownTextArea(attrs={"rows": 4, "style": 'width: 90%'})},
    }


class BigMarkdownTextArea(AdminMarkdownxWidget):
    template_name = 'markdownx/widget_big.html'


class QuestionAdminForm(ModelForm):
    class Meta:
        model = Question
        fields = "__all__"
        widgets = {
            "question_text": BigMarkdownTextArea(attrs={"cols": 10, "rows": 6, "style": 'width: 95%'}),
            "explanation_text": BigMarkdownTextArea(attrs={"cols": 10, "rows": 4, "style": 'width: 95%'}),
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
