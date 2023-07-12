from django.contrib import admin
from .models import Exam, NumTitle, Theme, TrainerTag


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
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