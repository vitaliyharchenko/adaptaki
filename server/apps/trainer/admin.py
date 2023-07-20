from django.contrib import admin
from .models import SubjectExamNumber, ExamTag


@admin.register(SubjectExamNumber)
class SubjectExamNumberAdmin(admin.ModelAdmin):
    pass


@admin.register(ExamTag)
class ExamTagAdmin(admin.ModelAdmin):
    list_filter = ["subject_exam_number", "is_active"]
    search_fields = ["title"]
