from django.core.management.base import AppCommand
from markdownx.utils import markdownify
from markdownx.utils import markdownify
import markdown
import mdx_math
from apps.questions.models import Question, QuestionOption


# Название класса обязательно - "Command"
class Command(AppCommand):
    # Используется как описание команды обычно
    help = 'Fond questions with zero true answers'

    def handle(self, *args, **kwargs):

        question = Question.objects.get(pk=12712)
        explanation_text = question.explanation_text

        md = markdown.Markdown(
            extensions=[mdx_math.makeExtension(enable_dollar_delimiter=True)])
        explanation_text_new = md.convert(explanation_text)

        explanation_text_new = explanation_text_new.replace(
            '<script type="math/tex">', '<span class="math-tex">\(')
        explanation_text_new = explanation_text_new.replace(
            '<script type="math/tex; mode=display">', '<span class="math-tex">\(')
        explanation_text_new = explanation_text_new.replace(
            '</script>', '\)</span>')

        question.explanation_text_new = explanation_text_new
        question.save()
