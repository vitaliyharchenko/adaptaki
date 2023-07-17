from django.core.management.base import AppCommand
from apps.questions.models import Question, QuestionOption


# Название класса обязательно - "Command"
class Command(AppCommand):
    # Используется как описание команды обычно
    help = 'Fond questions with zero true answers'

    def handle(self, *args, **kwargs):

        questions = Question.objects.all()
        one_counter = 0
        many_counter = 0
        zero_ids = []
        many_ids = []

        for q in questions:
            if q.type == 5:
                options = QuestionOption.objects.filter(question=q)

                true_counter = 0
                for opt in options:
                    if opt.is_true:
                        true_counter += 1

                if true_counter == 0:
                    zero_ids.append(q.pk)
                elif true_counter == 1:
                    one_counter += 1
                    q.type = 4
                    q.save()
                else:
                    many_counter += 1
                    many_ids.append(q.pk)
                    q.type = 5
                    q.save()

        print(f"One: {one_counter}, Many: {many_counter}")
        print(f"Zero answers: {zero_ids}")
