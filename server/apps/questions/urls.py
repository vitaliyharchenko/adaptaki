from django.urls import path
from . import views


urlpatterns = [
    # Api views
    path('questions/<int:pk>/', views.QuestionDetail.as_view()),
    path('questions/random', views.RandomQuestion.as_view()),

    # Template views
    path('questions/<int:pk>/html',
         views.QuestionHtmlView.as_view(), name='question_html'),
]
