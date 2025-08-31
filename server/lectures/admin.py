from django.contrib import admin
from django.utils.html import format_html
from .models import Lecture


@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ['title', 'get_entity_info', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at', 'node__subject', 'concept__subject']
    search_fields = ['title', 'content', 'node__title', 'concept__title']
    list_editable = ['order', 'is_active']
    readonly_fields = ['created_at', 'updated_at', 'vk_embed_preview']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'content')
        }),
        ('Привязка', {
            'fields': ('node', 'concept'),
            'description': 'Выберите либо узел, либо концепт для привязки лекции'
        }),
        ('Видео VK', {
            'fields': ('vk_video_url', 'vk_video_title', 'vk_embed_preview'),
            'classes': ('collapse',)
        }),
        ('Настройки', {
            'fields': ('order', 'is_active')
        }),
        ('Метаданные', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_entity_info(self, obj):
        """Отображает информацию о связанной сущности"""
        if obj.node:
            return format_html(
                '<span style="color: #007cba;">Узел:</span> {} ({})',
                obj.node.title,
                obj.node.get_type_display()
            )
        elif obj.concept:
            return format_html(
                '<span style="color: #28a745;">Концепт:</span> {}',
                obj.concept.title
            )
        return '-'
    get_entity_info.short_description = 'Связанная сущность'
    
    def vk_embed_preview(self, obj):
        """Предварительный просмотр VK видео"""
        if obj.vk_video_url:
            embed_code = obj.get_vk_embed_code()
            if embed_code:
                return format_html(
                    '<div style="margin: 10px 0;">'
                    '<strong>Предварительный просмотр:</strong><br>'
                    '{}'
                    '</div>',
                    embed_code
                )
            else:
                return format_html(
                    '<span style="color: #dc3545;">Неверный формат ссылки VK</span>'
                )
        return 'Видео не добавлено'
    vk_embed_preview.short_description = 'Предварительный просмотр видео'
    
    def get_queryset(self, request):
        """Оптимизация запросов"""
        return super().get_queryset(request).select_related('node', 'concept', 'node__subject', 'concept__subject')
    
    class Media:
        css = {
            'all': ('admin/css/lecture_admin.css',)
        }
        js = (
            'https://cdn.tiny.cloud/1/no-api-key/tinymce/6/tinymce.min.js',
            'admin/js/lecture_admin.js',
        )
