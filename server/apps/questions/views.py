from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from .models import Question
from .serializers import QuestionSerializer, QuestionAnswerSerializer


class QuestionDetail(APIView):
    """
    Задача по id
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Question.objects.get(pk=pk)
        except Question.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        question = self.get_object(pk)
        serializer = QuestionSerializer(question)
        return Response(serializer.data)


class QuestionAnswerCheck(APIView):
    """
    Проверка ответа на задание
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Question.objects.get(pk=pk)
        except Question.DoesNotExist:
            raise Http404
        
    def post(self, request, pk, format=None):
        serializer = QuestionAnswerSerializer(data=request.data)
        if serializer.is_valid():
            # Проверка правильности ответа и получение баллов
            answer = request.data["answer"]
            question = Question.objects.get(pk=pk)
            question.check_answer(answer)

            # сохранение результата с баллами

            return Response(request.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
