from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from .models import Question, QuestionOption


class QuestionOptionInline(admin.StackedInline):
    model = QuestionOption
    fk_name = "question"
    extra = 0


@admin.register(Question)
class QuestionAdmin(MarkdownxModelAdmin):
    inlines = [QuestionOptionInline]