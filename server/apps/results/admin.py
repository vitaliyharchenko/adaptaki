from django.contrib import admin
from .models import Result, StringResult


@admin.register(StringResult)
class StringResultAdmin(admin.ModelAdmin):
    pass
