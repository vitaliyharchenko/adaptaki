from django.contrib import admin
from .models import Exam, SubjectExam, SubjectExamNumber, NumTitle, Theme, TrainerTag


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


@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    pass


@admin.register(TrainerTag)
class TrainerTagAdmin(admin.ModelAdmin):
    pass
