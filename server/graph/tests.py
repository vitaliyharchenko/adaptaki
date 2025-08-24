from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Subject, Concept, Node, NodeRelation

User = get_user_model()


class GraphModelsTest(TestCase):
    """Тесты для моделей приложения graph"""

    def setUp(self):
        """Создание тестовых данных"""
        self.subject = Subject.objects.create(title="Математика")
        self.concept = Concept.objects.create(
            title="Квадратные уравнения",
            subject=self.subject,
            is_active=True
        )
        self.node1 = Node.objects.create(
            title="Квадратное уравнение",
            type="KN",
            subject=self.subject,
            concept=self.concept,
            testability=True
        )
        self.node2 = Node.objects.create(
            title="Дискриминант",
            type="KN",
            subject=self.subject,
            concept=self.concept,
            testability=True
        )
        self.relation = NodeRelation.objects.create(
            parent=self.node1,
            child=self.node2
        )

    def test_subject_creation(self):
        """Тест создания предмета"""
        self.assertEqual(self.subject.title, "Математика")
        self.assertEqual(str(self.subject), "Математика")

    def test_concept_creation(self):
        """Тест создания концепта"""
        self.assertEqual(self.concept.title, "Квадратные уравнения")
        self.assertEqual(self.concept.subject, self.subject)
        self.assertTrue(self.concept.is_active)
        self.assertIn(str(self.subject), str(self.concept))

    def test_node_creation(self):
        """Тест создания узла"""
        self.assertEqual(self.node1.title, "Квадратное уравнение")
        self.assertEqual(self.node1.type, "KN")
        self.assertEqual(self.node1.subject, self.subject)
        self.assertEqual(self.node1.concept, self.concept)
        self.assertTrue(self.node1.testability)
        self.assertIn(self.subject.title, str(self.node1))

    def test_node_relation_creation(self):
        """Тест создания связи между узлами"""
        self.assertEqual(self.relation.parent, self.node1)
        self.assertEqual(self.relation.child, self.node2)
        self.assertIn(self.node1.title[:20], str(self.relation))
        self.assertIn(self.node2.title[:20], str(self.relation))

    def test_unique_together_constraint(self):
        """Тест уникальности связи parent-child"""
        # Попытка создать дублирующую связь должна вызвать ошибку
        with self.assertRaises(Exception):
            NodeRelation.objects.create(parent=self.node1, child=self.node2)


class GraphSerializersTest(TestCase):
    """Тесты для сериализаторов"""

    def setUp(self):
        """Создание тестовых данных"""
        self.subject = Subject.objects.create(title="Физика")
        self.concept = Concept.objects.create(
            title="Механика",
            subject=self.subject,
            is_active=True
        )
        self.node = Node.objects.create(
            title="Скорость",
            type="KN",
            subject=self.subject,
            concept=self.concept,
            testability=True
        )

    def test_subject_serializer(self):
        """Тест сериализатора Subject"""
        from .serializers import SubjectSerializer
        serializer = SubjectSerializer(self.subject)
        data = serializer.data
        self.assertEqual(data['title'], "Физика")

    def test_concept_serializer(self):
        """Тест сериализатора Concept"""
        from .serializers import ConceptSerializer
        serializer = ConceptSerializer(self.concept)
        data = serializer.data
        self.assertEqual(data['title'], "Механика")
        self.assertEqual(data['subject'], self.subject.id)
        self.assertTrue(data['is_active'])

    def test_node_serializer(self):
        """Тест сериализатора Node"""
        from .serializers import NodeSerializer
        serializer = NodeSerializer(self.node)
        data = serializer.data
        self.assertEqual(data['title'], "Скорость")
        self.assertEqual(data['type'], "KN")
        self.assertEqual(data['subject'], self.subject.id)
        self.assertEqual(data['concept'], self.concept.id)
        self.assertTrue(data['testability'])


class GraphAPITest(APITestCase):
    """Тесты для API эндпоинтов"""

    def setUp(self):
        """Создание тестовых данных и пользователя"""
        # Создание пользователя
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )

        # Получение токена
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        # Создание тестовых данных
        self.subject = Subject.objects.create(title="Химия")
        self.concept = Concept.objects.create(
            title="Органическая химия",
            subject=self.subject,
            is_active=True
        )
        self.node = Node.objects.create(
            title="Углеводороды",
            type="KN",
            subject=self.subject,
            concept=self.concept,
            testability=True
        )

    def test_subjects_list(self):
        """Тест получения списка предметов"""
        url = reverse('subject-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], "Химия")

    def test_subject_create(self):
        """Тест создания предмета"""
        url = reverse('subject-list')
        data = {'title': 'Биология'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Subject.objects.count(), 2)
        self.assertEqual(response.data['title'], 'Биология')

    def test_concepts_list(self):
        """Тест получения списка концептов"""
        url = reverse('concept-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results']
                         [0]['title'], "Органическая химия")

    def test_concept_create(self):
        """Тест создания концепта"""
        url = reverse('concept-list')
        data = {
            'title': 'Неорганическая химия',
            'subject': self.subject.id,
            'is_active': True
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Concept.objects.count(), 2)

    def test_nodes_list(self):
        """Тест получения списка узлов"""
        url = reverse('node-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], "Углеводороды")

    def test_node_create(self):
        """Тест создания узла"""
        url = reverse('node-list')
        data = {
            'title': 'Алканы',
            'type': 'KN',
            'subject': self.subject.id,
            'concept': self.concept.id,
            'testability': True
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Node.objects.count(), 2)

    def test_node_filter_by_subject(self):
        """Тест фильтрации узлов по предмету"""
        url = reverse('node-list')
        response = self.client.get(url, {'subject': self.subject.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_node_filter_by_concept(self):
        """Тест фильтрации узлов по концепту"""
        url = reverse('node-list')
        response = self.client.get(url, {'concept': self.concept.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_node_search(self):
        """Тест поиска узлов по названию"""
        url = reverse('node-list')
        response = self.client.get(url, {'search': 'углеводороды'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_node_relations_list(self):
        """Тест получения списка связей"""
        # Создаем второй узел и связь
        node2 = Node.objects.create(
            title="Алканы",
            type="KN",
            subject=self.subject,
            concept=self.concept,
            testability=True
        )
        relation = NodeRelation.objects.create(parent=self.node, child=node2)

        url = reverse('noderelation-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_node_relation_create(self):
        """Тест создания связи между узлами"""
        # Создаем второй узел
        node2 = Node.objects.create(
            title="Алканы",
            type="KN",
            subject=self.subject,
            concept=self.concept,
            testability=True
        )

        url = reverse('noderelation-list')
        data = {
            'parent': self.node.id,
            'child': node2.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(NodeRelation.objects.count(), 1)

    def test_unauthorized_access(self):
        """Тест доступа без авторизации"""
        self.client.credentials()  # Убираем токен
        url = reverse('subject-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class GraphAdminTest(TestCase):
    """Тесты для админки"""

    def setUp(self):
        """Создание суперпользователя и тестовых данных"""
        self.admin_user = User.objects.create_superuser(
            email='admin@example.com',
            password='admin123'
        )
        self.subject = Subject.objects.create(title="История")
        self.concept = Concept.objects.create(
            title="Древний мир",
            subject=self.subject,
            is_active=True
        )
        self.node = Node.objects.create(
            title="Древний Египет",
            type="KN",
            subject=self.subject,
            concept=self.concept,
            testability=True
        )

    def test_subject_admin(self):
        """Тест админки для Subject"""
        from .admin import SubjectAdmin
        admin = SubjectAdmin(Subject, None)
        self.assertIn('title', admin.list_display)
        self.assertIn('title', admin.search_fields)

    def test_concept_admin(self):
        """Тест админки для Concept"""
        from .admin import ConceptAdmin
        admin = ConceptAdmin(Concept, None)
        self.assertIn('title', admin.list_display)
        self.assertIn('subject', admin.list_display)
        self.assertIn('is_active', admin.list_display)

    def test_node_admin(self):
        """Тест админки для Node"""
        from .admin import NodeAdmin
        admin = NodeAdmin(Node, None)
        self.assertIn('title', admin.list_display)
        self.assertIn('type', admin.list_display)
        self.assertIn('subject', admin.list_display)
