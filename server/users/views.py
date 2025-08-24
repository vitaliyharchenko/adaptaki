from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.conf import settings
from .serializers import UserSerializer, UserCreateSerializer, UserUpdateSerializer

User = get_user_model()


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]


class UserDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_profile(request):
    """Получить профиль текущего пользователя"""
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['GET'])
def social_auth_redirect(request):
    """Редирект после успешной социальной аутентификации"""
    return Response({
        'message': 'Успешная аутентификация через социальную сеть',
        'user_id': request.user.id if request.user.is_authenticated else None
    })
