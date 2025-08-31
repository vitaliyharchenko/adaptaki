from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.db import transaction

from .models import ExamType, ExamSubject, ExamNumber, ExamTopic
from graph.models import Subject
from questions.models import Question, QuestionType, GradingPolicy

User = get_user_model()


class ExamModelsTestCase(TestCase):
    """Тесты для моделей приложения exams"""

    def setUp(self):
        """Настройка тестовых данных"""
        # Создаем предметы
        self.math_subject = Subject.objects.create(title='Математика')
        self.physics_subject = Subject.objects.create(title='Физика')
        
        # Создаем типы экзаменов
        self.ege = ExamType.objects.create(
            name='ЕГЭ',
            description='Единый государственный экзамен',
            order=1
        )
        self.oge = ExamType.objects.create(
            name='ОГЭ',
            description='Основной государственный экзамен',
            order=2
        )
        
        # Создаем связи экзаменов с предметами
        self.ege_math = ExamSubject.objects.create(
            exam_type=self.ege,
            subject=self.math_subject,
            order=1
        )
        self.ege_physics = ExamSubject.objects.create(
            exam_type=self.ege,
            subject=self.physics_subject,
            order=2
        )
        
        # Создаем номера заданий
        self.task1 = ExamNumber.objects.create(
            exam_subject=self.ege_math,
            number=1,
            title='Планиметрия',
            description='Задачи на планиметрию',
            order=1
        )
        self.task2 = ExamNumber.objects.create(
            exam_subject=self.ege_math,
            number=2,
            title='Стереометрия',
            description='Задачи на стереометрию',
            order=2
        )
        
        # Создаем подтемы
        self.topic1 = ExamTopic.objects.create(
            exam_number=self.task1,
            title='Решение прямоугольного треугольника',
            description='Задачи на прямоугольные треугольники',
            order=1
        )
        self.topic2 = ExamTopic.objects.create(
            exam_number=self.task1,
            title='Площадь треугольника',
            description='Вычисление площади треугольника',
            order=2
        )

    def test_exam_type_creation(self):
        """Тест создания типа экзамена"""
        exam_type = ExamType.objects.create(
            name='Олимпиада',
            description='Всероссийская олимпиада',
            order=3
        )
        self.assertEqual(exam_type.name, 'Олимпиада')
        self.assertEqual(exam_type.description, 'Всероссийская олимпиада')
        self.assertTrue(exam_type.is_active)
        self.assertEqual(exam_type.order, 3)

    def test_exam_subject_creation(self):
        """Тест создания связи экзамена с предметом"""
        exam_subject = ExamSubject.objects.create(
            exam_type=self.oge,
            subject=self.math_subject,
            order=1
        )
        self.assertEqual(exam_subject.exam_type, self.oge)
        self.assertEqual(exam_subject.subject, self.math_subject)
        self.assertTrue(exam_subject.is_active)

    def test_exam_number_creation(self):
        """Тест создания номера задания"""
        exam_number = ExamNumber.objects.create(
            exam_subject=self.ege_physics,
            number=1,
            title='Механика',
            description='Задачи на механику',
            order=1
        )
        self.assertEqual(exam_number.number, 1)
        self.assertEqual(exam_number.title, 'Механика')
        self.assertEqual(exam_number.exam_subject, self.ege_physics)

    def test_exam_topic_creation(self):
        """Тест создания подтемы"""
        exam_topic = ExamTopic.objects.create(
            exam_number=self.task2,
            title='Объемы тел',
            description='Вычисление объемов',
            order=1
        )
        self.assertEqual(exam_topic.title, 'Объемы тел')
        self.assertEqual(exam_topic.exam_number, self.task2)

    def test_exam_type_str(self):
        """Тест строкового представления типа экзамена"""
        self.assertEqual(str(self.ege), 'ЕГЭ')

    def test_exam_subject_str(self):
        """Тест строкового представления предмета экзамена"""
        self.assertEqual(str(self.ege_math), 'ЕГЭ - Математика')

    def test_exam_number_str(self):
        """Тест строкового представления номера задания"""
        self.assertEqual(str(self.task1), 'Задание 1. Планиметрия')

    def test_exam_topic_str(self):
        """Тест строкового представления подтемы"""
        self.assertEqual(str(self.topic1), 'Решение прямоугольного треугольника')

    def test_exam_type_get_subjects(self):
        """Тест получения предметов для экзамена"""
        subjects = self.ege.get_subjects()
        self.assertEqual(subjects.count(), 2)
        self.assertIn(self.ege_math, subjects)
        self.assertIn(self.ege_physics, subjects)

    def test_exam_subject_get_numbers(self):
        """Тест получения номеров заданий для предмета"""
        numbers = self.ege_math.get_numbers()
        self.assertEqual(numbers.count(), 2)
        self.assertIn(self.task1, numbers)
        self.assertIn(self.task2, numbers)

    def test_exam_number_get_topics(self):
        """Тест получения подтем для номера задания"""
        topics = self.task1.get_topics()
        self.assertEqual(topics.count(), 2)
        self.assertIn(self.topic1, topics)
        self.assertIn(self.topic2, topics)

    def test_exam_number_get_full_path(self):
        """Тест получения полного пути к заданию"""
        full_path = self.task1.get_full_path()
        expected_path = 'ЕГЭ → Математика → Задание 1'
        self.assertEqual(full_path, expected_path)

    def test_exam_topic_get_full_path(self):
        """Тест получения полного пути к подтеме"""
        full_path = self.topic1.get_full_path()
        expected_path = 'ЕГЭ → Математика → Задание 1 → Решение прямоугольного треугольника'
        self.assertEqual(full_path, expected_path)

    def test_unique_constraints(self):
        """Тест уникальных ограничений"""
        # Попытка создать дублирующую связь экзамена с предметом
        with self.assertRaises(Exception):
            with transaction.atomic():
                ExamSubject.objects.create(
                    exam_type=self.ege,
                    subject=self.math_subject,
                    order=3
                )
        
        # Попытка создать дублирующий номер задания
        with self.assertRaises(Exception):
            with transaction.atomic():
                ExamNumber.objects.create(
                    exam_subject=self.ege_math,
                    number=1,  # Уже существует
                    title='Другое задание',
                    order=3
                )

    def test_ordering(self):
        """Тест сортировки"""
        # Создаем элементы с разным порядком
        exam_type3 = ExamType.objects.create(name='Тест', order=3)
        exam_type0 = ExamType.objects.create(name='Тест0', order=0)
        
        # Проверяем сортировку по умолчанию
        exam_types = ExamType.objects.all()
        self.assertEqual(exam_types[0], exam_type0)
        self.assertEqual(exam_types[1], self.ege)
        self.assertEqual(exam_types[2], self.oge)
        self.assertEqual(exam_types[3], exam_type3)


class ExamAPITestCase(APITestCase):
    """Тесты для API приложения exams"""

    def setUp(self):
        """Настройка тестовых данных"""
        # Создаем пользователя
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        # Создаем тестовые данные
        self.math_subject = Subject.objects.create(title='Математика')
        self.physics_subject = Subject.objects.create(title='Физика')
        
        self.ege = ExamType.objects.create(
            name='ЕГЭ',
            description='Единый государственный экзамен',
            order=1
        )
        
        self.ege_math = ExamSubject.objects.create(
            exam_type=self.ege,
            subject=self.math_subject,
            order=1
        )
        
        self.task1 = ExamNumber.objects.create(
            exam_subject=self.ege_math,
            number=1,
            title='Планиметрия',
            description='Задачи на планиметрию',
            order=1
        )
        
        self.topic1 = ExamTopic.objects.create(
            exam_number=self.task1,
            title='Решение прямоугольного треугольника',
            description='Задачи на прямоугольные треугольники',
            order=1
        )

    def test_exam_types_list(self):
        """Тест получения списка типов экзаменов"""
        url = reverse('exams:examtype-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'ЕГЭ')

    def test_exam_type_create(self):
        """Тест создания типа экзамена"""
        url = reverse('exams:examtype-list')
        data = {
            'name': 'ОГЭ',
            'description': 'Основной государственный экзамен',
            'order': 2
        }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ExamType.objects.count(), 2)
        self.assertEqual(response.data['name'], 'ОГЭ')

    def test_exam_type_detail(self):
        """Тест получения детальной информации о типе экзамена"""
        url = reverse('exams:examtype-detail', args=[self.ege.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'ЕГЭ')
        self.assertEqual(response.data['description'], 'Единый государственный экзамен')

    def test_exam_type_update(self):
        """Тест обновления типа экзамена"""
        url = reverse('exams:examtype-detail', args=[self.ege.id])
        data = {
            'name': 'ЕГЭ Обновленный',
            'description': 'Обновленное описание',
            'order': 1
        }
        response = self.client.put(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.ege.refresh_from_db()
        self.assertEqual(self.ege.name, 'ЕГЭ Обновленный')

    def test_exam_type_delete(self):
        """Тест удаления типа экзамена"""
        url = reverse('exams:examtype-detail', args=[self.ege.id])
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ExamType.objects.count(), 0)

    def test_exam_subjects_list(self):
        """Тест получения списка предметов экзаменов"""
        url = reverse('exams:examsubject-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['subject_name'], 'Математика')

    def test_exam_subject_create(self):
        """Тест создания предмета экзамена"""
        url = reverse('exams:examsubject-list')
        data = {
            'exam_type': self.ege.id,
            'subject': self.physics_subject.id,
            'order': 2
        }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ExamSubject.objects.count(), 2)

    def test_exam_numbers_list(self):
        """Тест получения списка номеров заданий"""
        url = reverse('exams:examnumber-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Планиметрия')

    def test_exam_number_create(self):
        """Тест создания номера задания"""
        url = reverse('exams:examnumber-list')
        data = {
            'exam_subject': self.ege_math.id,
            'number': 2,
            'title': 'Стереометрия',
            'description': 'Задачи на стереометрию',
            'order': 2
        }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ExamNumber.objects.count(), 2)

    def test_exam_topics_list(self):
        """Тест получения списка подтем"""
        url = reverse('exams:examtopic-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Решение прямоугольного треугольника')

    def test_exam_topic_create(self):
        """Тест создания подтемы"""
        url = reverse('exams:examtopic-list')
        data = {
            'exam_number': self.task1.id,
            'title': 'Площадь треугольника',
            'description': 'Вычисление площади треугольника',
            'order': 2
        }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ExamTopic.objects.count(), 2)

    def test_exam_type_subjects_action(self):
        """Тест получения предметов для конкретного экзамена"""
        url = reverse('exams:examtype-subjects', args=[self.ege.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['subject_name'], 'Математика')

    def test_exam_subject_numbers_action(self):
        """Тест получения номеров заданий для конкретного предмета"""
        url = reverse('exams:examsubject-numbers', args=[self.ege_math.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Планиметрия')

    def test_exam_number_topics_action(self):
        """Тест получения подтем для конкретного номера задания"""
        url = reverse('exams:examnumber-topics', args=[self.task1.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Решение прямоугольного треугольника')

    def test_navigation_endpoint(self):
        """Тест получения полной навигационной структуры"""
        url = reverse('exams:navigation-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('exam_types', response.data)
        self.assertEqual(len(response.data['exam_types']), 1)
        self.assertEqual(response.data['exam_types'][0]['name'], 'ЕГЭ')

    def test_filtering(self):
        """Тест фильтрации"""
        # Создаем неактивный тип экзамена
        inactive_exam = ExamType.objects.create(
            name='Неактивный',
            is_active=False
        )
        
        url = reverse('exams:examtype-list')
        response = self.client.get(url, {'is_active': 'true'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'ЕГЭ')

    def test_search(self):
        """Тест поиска"""
        url = reverse('exams:examtype-list')
        response = self.client.get(url, {'search': 'ЕГЭ'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'ЕГЭ')

    def test_ordering(self):
        """Тест сортировки"""
        # Создаем еще один тип экзамена с другим порядком
        ExamType.objects.create(name='ОГЭ', order=0)
        
        url = reverse('exams:examtype-list')
        response = self.client.get(url, {'ordering': 'order'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['name'], 'ОГЭ')
        self.assertEqual(response.data['results'][1]['name'], 'ЕГЭ')


class ExamTopicQuestionsTestCase(APITestCase):
    """Тесты для получения задач по подтемам"""

    def setUp(self):
        """Настройка тестовых данных"""
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        # Создаем структуру экзамена
        self.math_subject = Subject.objects.create(title='Математика')
        self.ege = ExamType.objects.create(name='ЕГЭ', order=1)
        self.ege_math = ExamSubject.objects.create(
            exam_type=self.ege,
            subject=self.math_subject,
            order=1
        )
        self.task1 = ExamNumber.objects.create(
            exam_subject=self.ege_math,
            number=1,
            title='Планиметрия',
            order=1
        )
        self.topic1 = ExamTopic.objects.create(
            exam_number=self.task1,
            title='Решение прямоугольного треугольника',
            order=1
        )
        
        # Создаем задачи
        self.question1 = Question.objects.create(
            title='Задача 1',
            condition='Найдите площадь прямоугольного треугольника с катетами 3 и 4',
            question_type=QuestionType.NUMBER,
            max_score=2,
            grading_policy=GradingPolicy.ALL_OR_NOTHING
        )
        self.question2 = Question.objects.create(
            title='Задача 2',
            condition='Найдите гипотенузу прямоугольного треугольника с катетами 5 и 12',
            question_type=QuestionType.NUMBER,
            max_score=2,
            grading_policy=GradingPolicy.ALL_OR_NOTHING
        )
        
        # Привязываем задачи к подтеме
        self.question1.exam_topics.add(self.topic1)
        self.question2.exam_topics.add(self.topic1)

    def test_exam_topic_questions_action(self):
        """Тест получения задач для подтемы"""
        url = reverse('exams:examtopic-questions', args=[self.topic1.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('topic', response.data)
        self.assertIn('questions', response.data)
        self.assertIn('questions_count', response.data)
        
        self.assertEqual(response.data['questions_count'], 2)
        self.assertEqual(len(response.data['questions']), 2)
        
        # Проверяем структуру данных задачи
        question_data = response.data['questions'][0]
        self.assertIn('id', question_data)
        self.assertIn('title', question_data)
        self.assertIn('condition', question_data)
        self.assertIn('question_type', question_data)
        self.assertIn('max_score', question_data)

    def test_exam_topic_questions_empty(self):
        """Тест получения задач для пустой подтемы"""
        # Создаем подтему без задач
        empty_topic = ExamTopic.objects.create(
            exam_number=self.task1,
            title='Пустая подтема',
            order=2
        )
        
        url = reverse('exams:examtopic-questions', args=[empty_topic.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['questions_count'], 0)
        self.assertEqual(len(response.data['questions']), 0)


class ExamSerializersTestCase(TestCase):
    """Тесты для сериализаторов"""

    def setUp(self):
        """Настройка тестовых данных"""
        self.math_subject = Subject.objects.create(title='Математика')
        self.ege = ExamType.objects.create(
            name='ЕГЭ',
            description='Единый государственный экзамен',
            order=1
        )
        self.ege_math = ExamSubject.objects.create(
            exam_type=self.ege,
            subject=self.math_subject,
            order=1
        )
        self.task1 = ExamNumber.objects.create(
            exam_subject=self.ege_math,
            number=1,
            title='Планиметрия',
            description='Задачи на планиметрию',
            order=1
        )
        self.topic1 = ExamTopic.objects.create(
            exam_number=self.task1,
            title='Решение прямоугольного треугольника',
            description='Задачи на прямоугольные треугольники',
            order=1
        )

    def test_exam_type_serializer(self):
        """Тест сериализатора типа экзамена"""
        from .serializers import ExamTypeSerializer
        
        serializer = ExamTypeSerializer(self.ege)
        data = serializer.data
        
        self.assertEqual(data['name'], 'ЕГЭ')
        self.assertEqual(data['description'], 'Единый государственный экзамен')
        self.assertEqual(data['order'], 1)
        self.assertTrue(data['is_active'])
        self.assertIn('subjects_count', data)

    def test_exam_subject_serializer(self):
        """Тест сериализатора предмета экзамена"""
        from .serializers import ExamSubjectSerializer
        
        serializer = ExamSubjectSerializer(self.ege_math)
        data = serializer.data
        
        self.assertEqual(data['exam_type'], self.ege.id)
        self.assertEqual(data['subject'], self.math_subject.id)
        self.assertEqual(data['exam_type_name'], 'ЕГЭ')
        self.assertEqual(data['subject_name'], 'Математика')
        self.assertIn('numbers_count', data)

    def test_exam_number_serializer(self):
        """Тест сериализатора номера задания"""
        from .serializers import ExamNumberSerializer
        
        serializer = ExamNumberSerializer(self.task1)
        data = serializer.data
        
        self.assertEqual(data['number'], 1)
        self.assertEqual(data['title'], 'Планиметрия')
        self.assertEqual(data['exam_subject'], self.ege_math.id)
        self.assertIn('exam_subject_info', data)
        self.assertIn('topics_count', data)

    def test_exam_topic_serializer(self):
        """Тест сериализатора подтемы"""
        from .serializers import ExamTopicSerializer
        
        serializer = ExamTopicSerializer(self.topic1)
        data = serializer.data
        
        self.assertEqual(data['title'], 'Решение прямоугольного треугольника')
        self.assertEqual(data['exam_number'], self.task1.id)
        self.assertIn('exam_number_info', data)
        self.assertIn('questions_count', data)
        self.assertIn('full_path', data)

    def test_navigation_serializer(self):
        """Тест сериализатора навигации"""
        from .serializers import NavigationSerializer
        
        serializer = NavigationSerializer(data={})
        serializer.is_valid()
        data = serializer.data
        
        self.assertIn('exam_types', data)
        self.assertEqual(len(data['exam_types']), 1)
        self.assertEqual(data['exam_types'][0]['name'], 'ЕГЭ')
