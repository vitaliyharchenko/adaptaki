from django.urls import path
from .views import GraphView, NodeView, NodeRelationView

urlpatterns = [
    # Маршрут для получения всего графа
    path('graph/', GraphView.as_view(), name='graph'),

    # Маршруты для работы с узлами
    path('nodes/', NodeView.as_view(), name='node-list'),
    path('nodes/<int:node_id>/', NodeView.as_view(), name='node-detail'),

    # Маршруты для работы с отношениями
    path('relations/', NodeRelationView.as_view(), name='relation-list'),
    path('relations/<int:relation_id>/',
         NodeRelationView.as_view(), name='relation-detail'),
]
