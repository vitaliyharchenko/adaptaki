from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LectureViewSet, upload_image

router = DefaultRouter()
router.register(r'lectures', LectureViewSet)

app_name = 'lectures'

urlpatterns = [
    path('', include(router.urls)),
    path('upload-image/', upload_image, name='upload_image'),
]
