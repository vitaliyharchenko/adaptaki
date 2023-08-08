from django.contrib import admin
from .models import SubjectExamNumber, ExamTag, Exam, SubjectExam

# @admin.register(SubjectExam)
# class SubjectExamAdmin(admin.ModelAdmin):
#     pass

# @admin.register(Exam)
# class ExamAdmin(admin.ModelAdmin):
#     pass


@admin.register(SubjectExamNumber)
class SubjectExamNumberAdmin(admin.ModelAdmin):
    pass


@admin.register(ExamTag)
class ExamTagAdmin(admin.ModelAdmin):
    list_filter = ["subject_exam_number", "is_active"]
    search_fields = ["title__icontains"]
