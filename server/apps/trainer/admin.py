from django.contrib import admin
from .models import SubjectExamNumber, ExamTag, Exam, SubjectExam
from apps.questions.models import Question
from django.utils.safestring import mark_safe

# @admin.register(SubjectExam)
# class SubjectExamAdmin(admin.ModelAdmin):
#     pass

# @admin.register(Exam)
# class ExamAdmin(admin.ModelAdmin):
#     pass


@admin.register(SubjectExamNumber)
class SubjectExamNumberAdmin(admin.ModelAdmin):
    pass


class QuestionInline(admin.TabularInline):
    model = Question
    fields = ['question_text', 'link_to_edit']
    readonly_fields = ['link_to_edit', 'question_text',]
    extra = 0
    show_change_link = True

    def link_to_edit(self, obj):
        url = f"/admin/questions/question/{obj.id}/change/"
        return mark_safe(f'<a href="{url}" target="_blank">Редактировать</a>')
    link_to_edit.short_description = "Открыть"


@admin.register(ExamTag)
class ExamTagAdmin(admin.ModelAdmin):
    list_filter = ["subject_exam_number", "is_active"]
    search_fields = ["title__icontains"]
    inlines = [QuestionInline]
