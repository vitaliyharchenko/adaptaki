from django.urls import path, include

from apps.graph.views import GraphView
from apps.questions.views import QuestionDetail, RandomQuestion
from apps.trainer.views import ExamTree

urlpatterns = [
    path('graph/', GraphView.as_view(), name='graph'),

    path('questions/<int:pk>/', QuestionDetail.as_view(), name='question_detail'),
    path('questions/random/', RandomQuestion.as_view(), name='random_question'),

    path('exam_tree/', ExamTree.as_view(), name='exam_tree'),
]
