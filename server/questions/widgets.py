from tinymce.widgets import TinyMCE
from django.conf import settings


class MathTinyMCE(TinyMCE):
    """
    Кастомный виджет TinyMCE
    """
    
    def __init__(self, *args, **kwargs):
        # Используем основную конфигурацию TinyMCE
        super().__init__(settings.TINYMCE_DEFAULT_CONFIG, *args, **kwargs)