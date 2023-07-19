from django.urls import path
from . import views


urlpatterns = [
    path('exam_tree/', views.ExamTree.as_view()),
    path('exam_tag-autocomplete/', views.ExamTagAutocomplete.as_view(), name='exam_tag-autocomplete'),
]
