from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from dal import autocomplete
from apps.graph.models import Subject
from .serializers import ExamTreeSerializer
from .models import ExamTag


class ExamTree(APIView):
    """
    Дерево экзаменов
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        subjects = Subject.objects.all()
        serializer = ExamTreeSerializer(subjects, many=True)
        return Response(serializer.data)
