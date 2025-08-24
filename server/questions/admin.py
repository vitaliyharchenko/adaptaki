from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from tinymce.widgets import TinyMCE
from .models import Question, QuestionOption, QuestionType, GradingPolicy


class QuestionOptionInline(admin.TabularInline):
    """Inline для вариантов ответов"""
    model = QuestionOption
    extra = 1
    fields = ['text', 'is_correct', 'order']
    ordering = ['order']

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'text':
            kwargs['widget'] = TinyMCE(attrs={'cols': 80, 'rows': 10})
        return super().formfield_for_dbfield(db_field, **kwargs)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Админка для задач"""
    list_display = [
        'get_display_title',
        'question_type',
        'max_score',
        'grading_policy',
        'is_active',
        'created_at',
        'correct_answers_count',
        'options_count'
    ]

    list_filter = [
        'question_type',
        'grading_policy',
        'is_active',
        'created_at',
        'nodes__subject',
        'nodes__concept'
    ]

    search_fields = ['title', 'condition', 'solution']

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'condition', 'solution', 'is_active')
        }),
        ('Тип и настройки', {
            'fields': ('question_type', 'max_score', 'grading_policy', 'precision')
        }),
        ('Связи', {
            'fields': ('nodes', 'analogs'),
            'classes': ('collapse',)
        }),
        ('Метаданные', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ['created_at', 'updated_at']

    inlines = [QuestionOptionInline]

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name in ['condition', 'solution']:
            kwargs['widget'] = TinyMCE(attrs={'cols': 80, 'rows': 20})
        return super().formfield_for_dbfield(db_field, **kwargs)

    actions = ['copy_questions', 'activate_questions', 'deactivate_questions']

    def correct_answers_count(self, obj):
        """Количество правильных ответов"""
        count = obj.options.filter(is_correct=True).count()
        return format_html(
            '<span style="color: green;">{}</span>',
            count
        )
    correct_answers_count.short_description = 'Правильных ответов'

    def options_count(self, obj):
        """Общее количество вариантов ответов"""
        return obj.options.count()
    options_count.short_description = 'Всего вариантов'

    def get_display_title(self, obj):
        """Отображает название задачи"""
        if obj.title:
            return obj.title
        else:
            auto_title = obj.get_auto_title()
            return format_html('<span style="color: #666; font-style: italic;">{}</span>', auto_title)
    get_display_title.short_description = 'Название'

    def copy_questions(self, request, queryset):
        """Копировать выбранные задачи"""
        copied_count = 0
        for question in queryset:
            # Создаем копию задачи
            new_question = Question.objects.create(
                title=f"{question.title} (копия)",
                condition=question.condition,
                solution=question.solution,
                question_type=question.question_type,
                max_score=question.max_score,
                grading_policy=question.grading_policy,
                precision=question.precision,
                is_active=False  # Копия неактивна по умолчанию
            )

            # Копируем связи
            new_question.nodes.set(question.nodes.all())
            new_question.analogs.set(question.analogs.all())

            # Копируем варианты ответов
            for option in question.options.all():
                QuestionOption.objects.create(
                    question=new_question,
                    text=option.text,
                    is_correct=option.is_correct,
                    order=option.order
                )

            copied_count += 1

        self.message_user(
            request,
            f'Успешно скопировано {copied_count} задач'
        )
    copy_questions.short_description = 'Копировать выбранные задачи'

    def activate_questions(self, request, queryset):
        """Активировать выбранные задачи"""
        updated = queryset.update(is_active=True)
        self.message_user(
            request,
            f'Активировано {updated} задач'
        )
    activate_questions.short_description = 'Активировать выбранные задачи'

    def deactivate_questions(self, request, queryset):
        """Деактивировать выбранные задачи"""
        updated = queryset.update(is_active=False)
        self.message_user(
            request,
            f'Деактивировано {updated} задач'
        )
    deactivate_questions.short_description = 'Деактивировать выбранные задачи'

    def get_queryset(self, request):
        """Оптимизация запросов"""
        return super().get_queryset(request).prefetch_related(
            'options', 'nodes', 'analogs'
        )


@admin.register(QuestionOption)
class QuestionOptionAdmin(admin.ModelAdmin):
    """Админка для вариантов ответов (отдельно)"""
    list_display = ['question', 'text_preview', 'is_correct', 'order']
    list_filter = ['is_correct', 'question__question_type']
    search_fields = ['text', 'question__title']
    ordering = ['question', 'order']

    def text_preview(self, obj):
        """Предварительный просмотр текста"""
        return obj.text[:100] + '...' if len(obj.text) > 100 else obj.text
    text_preview.short_description = 'Текст'
