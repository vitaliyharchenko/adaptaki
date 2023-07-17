from django.contrib import admin
from .models import Result, StringResult, ChoiceResult


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    pass


@admin.register(StringResult)
class StringResultAdmin(admin.ModelAdmin):
    pass


@admin.register(ChoiceResult)
class ChoiceResultAdmin(admin.ModelAdmin):
    pass
