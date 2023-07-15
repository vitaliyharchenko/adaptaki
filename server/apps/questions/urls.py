from django.urls import path
from . import views


urlpatterns = [
    path('questions/<int:pk>/', views.QuestionDetail.as_view()),
]
