from django.core.management.base import BaseCommand
from apps.trainer.models import SubjectExam, SubjectExamNumber
from apps.questions.models import Question
import json


# Название класса обязательно - "Command"
class Command(BaseCommand):
    # Используется как описание команды обычно
    help = 'Implemented to Django application telegram bot setup command'

    def handle(self, *args, **kwargs):
        f = open('fixtures/old/questions.json')
        data = json.load(f)

        float_qs = []

        for d in data:
            if d['model'] == 'questions.floatanswerquestion':
                float_qs.append(d)
        print(float_qs[-1])

        # for q in float_qs:
        #     query = Question.objects.get(pk=q["pk"])
        #     query.type = 7
        #     query.save()
        