from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ExamTypeViewSet, ExamSubjectViewSet, 
    ExamNumberViewSet, ExamTopicViewSet, NavigationViewSet
)

router = DefaultRouter()
router.register(r'exam-types', ExamTypeViewSet)
router.register(r'exam-subjects', ExamSubjectViewSet)
router.register(r'exam-numbers', ExamNumberViewSet)
router.register(r'exam-topics', ExamTopicViewSet)
router.register(r'navigation', NavigationViewSet, basename='navigation')

app_name = 'exams'

urlpatterns = [
    path('api/exams/', include(router.urls)),
]
