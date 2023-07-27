from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from dal import autocomplete
from apps.graph.models import Subject
from .serializers import ExamTreeSerializer
from .models import Exam


class ExamTree(APIView):
    """
    Дерево экзаменов
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        exams = Exam.objects.all()
        serializer = ExamTreeSerializer(exams, many=True)
        return Response(serializer.data)
