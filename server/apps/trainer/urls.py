from django.urls import path
from . import views


urlpatterns = [
    path('exam_tree/', views.ExamTree.as_view()),
]
