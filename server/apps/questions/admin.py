from django.contrib import admin
from django.db import models
from django.forms import ModelForm
from markdownx.widgets import AdminMarkdownxWidget
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
            "question_text": Textarea(),
            "explanation_text": Textarea(),
        }


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [QuestionOptionInline]
    form = QuestionAdminForm
    list_filter = ["exam_tag", "type"]
    fieldsets = [
        ("Тип задачи", {"fields": [
            "type", "max_score", "checking_policy"]}),
        ("Условие задачи", {"fields": ["question_text", "image"]}),
        ("Пояснение", {"fields": [
            "explanation_text", "explanation_image"]}),
        ("Привязка", {"fields": [
            "nodes", "exam_tag"], "classes": ["collapse"]}),
    ]
