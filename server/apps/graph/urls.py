from django.urls import path
from . import views


urlpatterns = [
    path('graph/', views.GraphView.as_view()),
    path('node-autocomplete/$', views.NodeAutocomplete.as_view(), name='node-autocomplete'),
]
