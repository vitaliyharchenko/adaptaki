from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubjectViewSet, ConceptViewSet, NodeViewSet, NodeRelationViewSet

router = DefaultRouter()
router.register(r'subjects', SubjectViewSet)
router.register(r'concepts', ConceptViewSet)
router.register(r'nodes', NodeViewSet)
router.register(r'node-relations', NodeRelationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
