from django.core.management.base import AppCommand
from markdownx.utils import markdownify
import markdown
from apps.questions.models import Question, QuestionOption


# Название класса обязательно - "Command"
class Command(AppCommand):
    # Используется как описание команды обычно
    help = 'Fond questions with zero true answers'

    def handle(self, *args, **kwargs):

        question = Question.objects.get(pk=12782)

        # question_text = markdownify(question.question_text)
        question_text = markdown.markdown(
            question.question_text, extensions=['mdx_math'])
        question_text_new = question.question_text_new

        print(f"{question_text}")
        print(f"***")
        print(f"{question_text_new}")
