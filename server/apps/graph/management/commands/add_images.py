from django.core.management.base import BaseCommand
from apps.trainer.models import SubjectExam, SubjectExamNumber
from apps.questions.models import Question
import json


# Название класса обязательно - "Command"
class Command(BaseCommand):
    # Используется как описание команды обычно
    help = 'Implemented to Django application telegram bot setup command'

    def handle(self, *args, **kwargs):
        questions = Question.objects.all()
        for question in questions:
            image_url = question.image
            if image_url:
                question_text_new = question.question_text_new
                string = f'<p><img alt="" height="200" src="/media/{image_url}"/></p>'
                print(question_text_new + string)
                question.question_text_new = question_text_new + string
                question.save()
