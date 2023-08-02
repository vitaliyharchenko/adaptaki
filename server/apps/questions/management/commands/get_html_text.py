from django.core.management.base import AppCommand
from markdownx.utils import markdownify
from markdown_katex.extension import tex2html
from html2image import Html2Image
import markdown
import imgkit
from apps.questions.models import Question, QuestionOption


# Название класса обязательно - "Command"
class Command(AppCommand):
    # Используется как описание команды обычно
    help = 'Fond questions with zero true answers'

    def handle(self, *args, **kwargs):

        questions = Question.objects.filter(pk__in=[10674, 2, 12782])

        for question in questions:

            # url = f'http://127.0.0.1:8000/questions/{question.pk}/html'
            # img = imgkit.from_url(url, f'question_{question.pk}.png', options={
            #     'javascript-delay': 2000
            # })

            hti = Html2Image()

            hti.screenshot(url=f'http://127.0.0.1:8000/questions/{question.pk}/html', save_as=f'question_{question.pk}.png', size=(600, 500))
