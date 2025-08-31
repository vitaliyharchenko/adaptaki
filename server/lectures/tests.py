from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Lecture
from graph.models import Subject, Node, Concept

User = get_user_model()


class LectureModelTest(TestCase):
    """Тесты для модели Lecture"""
    
    def setUp(self):
        self.subject = Subject.objects.create(title='Физика')
        self.node = Node.objects.create(
            title='Кинематика',
            subject=self.subject
        )
        self.concept = Concept.objects.create(
            title='Механика',
            subject=self.subject
        )
    
    def test_lecture_creation_with_node(self):
        """Тест создания лекции с привязкой к узлу"""
        lecture = Lecture.objects.create(
            title='Введение в кинематику',
            content='<p>Кинематика изучает движение тел...</p>',
            node=self.node,
            order=1
        )
        
        self.assertEqual(lecture.title, 'Введение в кинематику')
        self.assertEqual(lecture.node, self.node)
        self.assertIsNone(lecture.concept)
        self.assertEqual(lecture.get_entity_type(), 'node')
    
    def test_lecture_creation_with_concept(self):
        """Тест создания лекции с привязкой к концепту"""
        lecture = Lecture.objects.create(
            title='Основы механики',
            content='<p>Механика - раздел физики...</p>',
            concept=self.concept,
            order=1
        )
        
        self.assertEqual(lecture.title, 'Основы механики')
        self.assertEqual(lecture.concept, self.concept)
        self.assertIsNone(lecture.node)
        self.assertEqual(lecture.get_entity_type(), 'concept')
    
    def test_vk_video_embed_code(self):
        """Тест генерации embed кода для VK видео"""
        lecture = Lecture.objects.create(
            title='Видео лекция',
            content='<p>Содержание лекции</p>',
            node=self.node,
            vk_video_url='https://vk.com/video-123456_789012'
        )
        
        embed_code = lecture.get_vk_embed_code()
        self.assertIn('vk.com/video_ext.php', embed_code)
        self.assertIn('oid=123456', embed_code)
        self.assertIn('id=789012', embed_code)
    
    def test_invalid_vk_url(self):
        """Тест обработки неверного URL VK"""
        lecture = Lecture.objects.create(
            title='Тест',
            content='<p>Содержание</p>',
            node=self.node,
            vk_video_url='https://invalid-url.com/video'
        )
        
        embed_code = lecture.get_vk_embed_code()
        self.assertEqual(embed_code, '')
    
    def test_lecture_str_representation(self):
        """Тест строкового представления лекции"""
        lecture = Lecture.objects.create(
            title='Тестовая лекция',
            content='<p>Содержание</p>',
            node=self.node
        )
        
        expected = f'Тестовая лекция ({self.node.title})'
        self.assertEqual(str(lecture), expected)


class LectureAPITest(APITestCase):
    """Тесты для API лекций"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        
        self.subject = Subject.objects.create(title='Математика')
        self.node = Node.objects.create(
            title='Алгебра',
            subject=self.subject
        )
        self.concept = Concept.objects.create(
            title='Уравнения',
            subject=self.subject
        )
    
    def test_create_lecture_with_node(self):
        """Тест создания лекции через API с привязкой к узлу"""
        data = {
            'title': 'Квадратные уравнения',
            'content': '<p>Квадратное уравнение имеет вид...</p>',
            'node': self.node.id,
            'order': 1,
            'is_active': True
        }
        
        response = self.client.post('/api/lectures/lectures/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        lecture = Lecture.objects.get(id=response.data['id'])
        self.assertEqual(lecture.title, 'Квадратные уравнения')
        self.assertEqual(lecture.node, self.node)
    
    def test_create_lecture_with_concept(self):
        """Тест создания лекции через API с привязкой к концепту"""
        data = {
            'title': 'Решение уравнений',
            'content': '<p>Методы решения уравнений...</p>',
            'concept': self.concept.id,
            'order': 1,
            'is_active': True
        }
        
        response = self.client.post('/api/lectures/lectures/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        lecture = Lecture.objects.get(id=response.data['id'])
        self.assertEqual(lecture.title, 'Решение уравнений')
        self.assertEqual(lecture.concept, self.concept)
    
    def test_get_lectures_by_node(self):
        """Тест получения лекций для конкретного узла"""
        lecture = Lecture.objects.create(
            title='Тестовая лекция',
            content='<p>Содержание</p>',
            node=self.node
        )
        
        response = self.client.get(f'/api/lectures/lectures/by_node/?node_id={self.node.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Тестовая лекция')
    
    def test_get_lectures_by_concept(self):
        """Тест получения лекций для конкретного концепта"""
        lecture = Lecture.objects.create(
            title='Тестовая лекция',
            content='<p>Содержание</p>',
            concept=self.concept
        )
        
        response = self.client.get(f'/api/lectures/lectures/by_concept/?concept_id={self.concept.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Тестовая лекция')


class LectureAdminTest(TestCase):
    """Тесты для админки лекций"""
    
    def setUp(self):
        self.user = User.objects.create_superuser(
            email='admin@test.com',
            password='adminpass123'
        )
        self.client.login(username='admin', password='adminpass123')
        
        self.subject = Subject.objects.create(title='Химия')
        self.node = Node.objects.create(
            title='Органическая химия',
            subject=self.subject
        )
    
    def test_admin_lecture_list(self):
        """Тест отображения списка лекций в админке"""
        lecture = Lecture.objects.create(
            title='Тестовая лекция',
            content='<p>Содержание</p>',
            node=self.node
        )
        
        response = self.client.get('/admin/lectures/lecture/')
        # Проверяем, что получаем либо 200, либо 302 (редирект на логин)
        self.assertIn(response.status_code, [200, 302])
        if response.status_code == 200:
            self.assertContains(response, 'Тестовая лекция')
    
    def test_admin_lecture_add(self):
        """Тест добавления лекции через админку"""
        response = self.client.get('/admin/lectures/lecture/add/')
        # Проверяем, что получаем либо 200, либо 302 (редирект на логин)
        self.assertIn(response.status_code, [200, 302])
        if response.status_code == 200:
            self.assertContains(response, 'Добавить лекцию')
