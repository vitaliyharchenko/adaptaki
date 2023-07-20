from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from .models import Question
from .serializers import QuestionSerializer, QuestionAnswerSerializer, QuestionSerializerWithAnswer


class QuestionDetail(APIView):
    """
        get:
        
        Возвращает сериализованный вопрос
        
        Можно указать также параметр answer=True (/&answer=True) для получения списка ответов


        post:

        Проверяет вариант ответа
        Этот метод принимает JSON формата:

        {
            "answer": "123" // для строк, чисел и набора символов, выбора одного варианта
            "answer": "123,124" // для выбора нескольких вариантов
        }

    """
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Question.objects.get(pk=pk)
        except Question.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        question = self.get_object(pk)
        need_answer = request.GET.get('answer', False)
        print(f"need answer: {need_answer}")
        if need_answer:
            serializer = QuestionSerializerWithAnswer(question)
        else:
            serializer = QuestionSerializer(question)
        return Response(serializer.data)
    
    def post(self, request, pk, format=None):
        serializer = QuestionAnswerSerializer(data=request.data)
        if serializer.is_valid():
            # Проверка правильности ответа и получение баллов
            answer = request.data["answer"]

            # TODO: распознать пользователя по запросу
            user = request.user
            question = Question.objects.get(pk=pk)
            score = question.check_answer(answer, user=user)

            return Response({'data': request.data, "score": score}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RandomQuestion(APIView):
    """
    Рандомный вопрос

    Возможна фильтрация по type, nodes, exam_tag
    Можно указать также параметр answer=True (/&answer=True) для получения списка ответов
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, request):
        try:
            type = self.request.GET.get('type', None)
            exam_tag = self.request.GET.get('exam_tag', None)

            query = Question.objects.all()

            if type:
                query = query.filter(type=type)
            
            if exam_tag:
                query = query.filter(exam_tag_id=exam_tag)

            return query.order_by('?')[0]
        except Question.DoesNotExist:
            raise Http404
        except IndexError:
            raise Http404
        
    def get(self, request, format=None):
        question = self.get_object(request)
        need_answer = request.GET.get('answer', False)

        if need_answer:
            serializer = QuestionSerializerWithAnswer(question)
        else:
            serializer = QuestionSerializer(question)
        return Response(serializer.data)
        

