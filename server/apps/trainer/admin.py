from django.contrib import admin
from .models import Exam, SubjectExam, SubjectExamNumber, NumTitle, ExamTag, TrainerTag


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    pass


@admin.register(SubjectExam)
class SubjectExamAdmin(admin.ModelAdmin):
    pass


@admin.register(SubjectExamNumber)
class SubjectExamNumberAdmin(admin.ModelAdmin):
    pass


@admin.register(NumTitle)
class NumTitleAdmin(admin.ModelAdmin):
    pass


@admin.register(ExamTag)
class ExamTagAdmin(admin.ModelAdmin):
    list_filter = ["subject_exam_number", "is_active"]


@admin.register(TrainerTag)
class TrainerTagAdmin(admin.ModelAdmin):
    list_filter = ["subject", "exam", "num"]
