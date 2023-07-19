from django.urls import path
from . import views


urlpatterns = [
    path('questions/<int:pk>/', views.QuestionDetail.as_view()),
    path('questions/<int:pk>/check', views.QuestionAnswerCheck.as_view()),
]
