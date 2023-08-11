from django.core.management.base import AppCommand
from markdownx.utils import markdownify
from markdownx.utils import markdownify
import markdown
import mdx_math
from django.template.loader import render_to_string
import imgkit
from apps.questions.models import Question, QuestionOption


# Название класса обязательно - "Command"
class Command(AppCommand):
    # Используется как описание команды обычно
    help = 'Fond questions with zero true answers'

    def handle(self, *args, **kwargs):

        question = Question.objects.get(pk=12545)

        html = render_to_string('questions/question.html', {'question': question})

        html = html.replace("/media/", "/code/mediafiles/")

        # imgkit.from_url(f'http://web:8000/questions/{question.pk}/html', 'out.jpg')
        imgkit.from_string(html, 'out.jpg', options={"enable-local-file-access": "", "crop-w": 630})

        # question_text = question.question_text

        # extension_configs = {
        #     'mdx_math_svg': {
        #         'inline_class': 'math',
        #         'display_class': 'math'
        #     }
        # }
        # md = markdown.Markdown(extensions=['mdx_math_svg'], extension_configs=extension_configs)

        # svg_text = md.convert(question_text)

        # print(svg_text)

        # questions = Question.objects.all()

        # for question in questions:
        #     question_text = question.question_text_new
        #     explanation_text = question.explanation_text

            # md = markdown.Markdown(
            #     extensions=[mdx_math.makeExtension(enable_dollar_delimiter=True)])
            # explanation_text_new = md.convert(explanation_text)

            # question_text_new = question_text.replace(
            #     '<img alt="" width="400"', '<img alt="" width="600"')
            # question.question_text_new = question_text_new

            # explanation_text_new = explanation_text_new.replace(
            #     '<script type="math/tex">', '<span class="math-tex">\(')
            # explanation_text_new = explanation_text_new.replace(
            #     '<script type="math/tex; mode=display">', '<span class="math-tex">\(')
            # explanation_text_new = explanation_text_new.replace(
            #     '</script>', '\)</span>')

            # if question.explanation_image:
            #     explanation_text_new += f'<p><img alt="" width="400" src="/media/{question.explanation_image}"/></p>'

            # question.explanation_text_new = explanation_text_new
            # question.save()
