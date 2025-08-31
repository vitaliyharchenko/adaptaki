import re
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from graph.models import Node, Concept


class Lecture(models.Model):
    """
    Мини-лекция, привязанная к Node или Concept
    Поддерживает HTML контент с изображениями, LaTeX формулы и VK видео
    """
    title = models.CharField(
        max_length=300, 
        verbose_name='Название лекции'
    )
    
    content = models.TextField(
        verbose_name='Содержание лекции',
        help_text='Используйте редактор для добавления текста, изображений и формул'
    )
    
    # Привязка к одной сущности (либо Node, либо Concept)
    node = models.ForeignKey(
        Node, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        verbose_name='Привязанный узел'
    )
    
    concept = models.ForeignKey(
        Concept, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        verbose_name='Привязанный концепт'
    )
    
    # Видео с VK
    vk_video_url = models.URLField(
        blank=True, 
        verbose_name='Ссылка на видео VK',
        help_text='Вставьте ссылку на видео с VK (например: https://vk.com/video-123456_789012)'
    )
    
    vk_video_title = models.CharField(
        max_length=200, 
        blank=True, 
        verbose_name='Название видео'
    )
    
    # Метаданные
    order = models.PositiveIntegerField(
        default=0, 
        verbose_name='Порядок отображения'
    )
    
    is_active = models.BooleanField(
        default=True, 
        verbose_name='Активна?'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )
    
    class Meta:
        verbose_name = 'лекция'
        verbose_name_plural = 'лекции'
        ordering = ['order', 'title']
        constraints = [
            models.CheckConstraint(
                check=models.Q(node__isnull=False, concept__isnull=True) | 
                      models.Q(node__isnull=True, concept__isnull=False),
                name='lecture_single_entity'
            )
        ]
    
    def __str__(self):
        entity = self.node.title if self.node else self.concept.title
        return f"{self.title} ({entity})"
    
    def clean(self):
        """Валидация модели"""
        super().clean()
        
        # Проверяем, что лекция привязана ровно к одной сущности
        if bool(self.node) == bool(self.concept):
            raise ValidationError(
                _('Лекция должна быть привязана либо к узлу, либо к концепту, но не к обоим')
            )
        
        # Проверяем формат VK видео URL
        if self.vk_video_url and not self._is_valid_vk_url(self.vk_video_url):
            raise ValidationError(
                _('Неверный формат ссылки на видео VK')
            )
    
    def _is_valid_vk_url(self, url):
        """Проверяет корректность URL видео VK"""
        vk_patterns = [
            r'https?://vk\.com/video-\d+_\d+',
            r'https?://vk\.com/video\d+_\d+',
            r'https?://vk\.com/clip-\d+_\d+',
        ]
        
        return any(re.match(pattern, url) for pattern in vk_patterns)
    
    def get_vk_embed_code(self):
        """Получить embed код для VK видео"""
        if not self.vk_video_url:
            return ""
        
        # Извлекаем ID видео из URL VK
        video_id_match = re.search(r'video-?\d+_(\d+)', self.vk_video_url)
        if video_id_match:
            video_id = video_id_match.group(1)
            owner_id_match = re.search(r'video-?(\d+)_', self.vk_video_url)
            owner_id = owner_id_match.group(1) if owner_id_match else '0'
            
            return f'<iframe src="https://vk.com/video_ext.php?oid={owner_id}&id={video_id}&hd=1" width="853" height="480" allow="autoplay; encrypted-media; fullscreen; picture-in-picture;" frameborder="0" allowfullscreen></iframe>'
        
        return ""
    
    def get_entity(self):
        """Получить связанную сущность (Node или Concept)"""
        return self.node or self.concept
    
    def get_entity_type(self):
        """Получить тип связанной сущности"""
        return 'node' if self.node else 'concept'
