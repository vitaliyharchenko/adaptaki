from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from apps.graph.views import GraphView, NodeView, NodeRelationView
from apps.questions.views import QuestionDetail, RandomQuestion
from apps.trainer.views import ExamTree
from apps.users.views import GetUserProfile, MyTokenView

urlpatterns = [
    path('graph/', GraphView.as_view(), name='graph'),

    path('nodes/', NodeView.as_view(), name='node-list'),
    path('nodes/<int:node_id>/', NodeView.as_view(), name='node-detail'),

    path('relations/', NodeRelationView.as_view(), name='relation-list'),
    path('relations/<int:relation_id>/',
         NodeRelationView.as_view(), name='relation-detail'),

    path('questions/<int:pk>/', QuestionDetail.as_view(), name='question_detail'),
    path('questions/random/', RandomQuestion.as_view(), name='random_question'),

    path('exam_tree/', ExamTree.as_view(), name='exam_tree'),

    path('users/me/', GetUserProfile.as_view(), name='user_profile'),

    path('token/', MyTokenView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
