from django.core.management.base import BaseCommand
from apps.trainer.models import SubjectExam, TrainerTag, SubjectExamNumber
from apps.questions.models import Question, QuestionOption


# Название класса обязательно - "Command"
class Command(BaseCommand):
    # Используется как описание команды обычно
    help = 'Implemented to Django application telegram bot setup command'

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
                        true_counter = 1
                if true_counter == 0:
                    zero_ids.append(q.pk)
                elif true_counter == 1:
                    one_counter += 1
                else:
                    many_counter += 1
                    many_ids.append(q.pk)

        print(f"One: {one_counter}, Many: {many_counter}")
        print(many_ids)
        print(zero_ids)

        # subject_exams = SubjectExam.objects.all()

        # trainer_tags = TrainerTag.objects.all()

        # tag_ids = []

        # for tag in trainer_tags:
        #     if tag.pk not in tag_ids:
        #         tag_ids.append(tag.pk)

        #         theme = tag.theme

        #         print(f'Search for {tag.exam} {tag.subject} {tag.num}')
        #         se = SubjectExam.objects.get(
        #             exam=tag.exam, subject=tag.subject)
        #         sen = SubjectExamNumber.objects.get(
        #             subject_exam=se, num=tag.num)

        #         # print(tag, tag.theme, sen, tag.is_active)
        #         theme.subject_exam_number = sen
        #         theme.is_active = tag.is_active
        #         theme.save()

        # array = []

        # for subject_exam in subject_exams:
        #     print(f'***SubjectExam: {subject_exam}')
        #     s_e = {
        #         'subject_exam': subject_exam.pk,
        #         'nums_ids': [],
        #         'nums': []
        #     }
        #     for trainer_tag in trainer_tags:
        #         if trainer_tag.subject == subject_exam.subject:
        #             if trainer_tag.exam == subject_exam.exam:
        #                 if trainer_tag.num not in s_e['nums_ids']:
        #                     s_e['nums_ids'].append(trainer_tag.num)
        #                     s_e['nums'].append({
        #                         'num': trainer_tag.num,
        #                         'title': trainer_tag.num_title
        #                     })
        #                     obj = SubjectExamNumber.objects.create(
        #                         subject_exam=subject_exam, num=trainer_tag.num, title=trainer_tag.num_title)
        #     array.append(s_e)
        # print(array)
