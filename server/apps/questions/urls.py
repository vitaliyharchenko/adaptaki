from django.urls import path
from . import views


urlpatterns = [
    path('questions/<int:pk>/html',
         views.QuestionHtmlView.as_view(), name='question_html'),
]
