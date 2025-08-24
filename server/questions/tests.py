from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Question, QuestionOption, QuestionType, GradingPolicy
from graph.models import Subject, Concept, Node

User = get_user_model()


class QuestionModelTest(TestCase):
    """Тесты для модели Question"""

    def setUp(self):
        self.subject = Subject.objects.create(title='Математика')
        self.concept = Concept.objects.create(
            title='Квадратные уравнения',
            subject=self.subject
        )
        self.node = Node.objects.create(
            title='Решение квадратных уравнений',
            subject=self.subject,
            concept=self.concept
        )

        self.question = Question.objects.create(
            title='Решите уравнение x² + 5x + 6 = 0',
            condition='<p>Найдите корни квадратного уравнения:</p><p>x² + 5x + 6 = 0</p>',
            solution='<p>Используя формулу дискриминанта...</p>',
            question_type=QuestionType.NUMBER,
            max_score=2,
            grading_policy=GradingPolicy.ALL_OR_NOTHING
        )
        self.question.nodes.add(self.node)

        # Создаем варианты ответов
        QuestionOption.objects.create(
            question=self.question,
            text='-2',
            is_correct=True,
            order=1
        )
        QuestionOption.objects.create(
            question=self.question,
            text='-3',
            is_correct=True,
            order=2
        )
        QuestionOption.objects.create(
            question=self.question,
            text='2',
            is_correct=False,
            order=3
        )

    def test_question_creation(self):
        """Тест создания задачи"""
        self.assertEqual(self.question.title,
                         'Решите уравнение x² + 5x + 6 = 0')
        self.assertEqual(self.question.question_type, QuestionType.NUMBER)
        self.assertEqual(self.question.max_score, 2)
        self.assertTrue(self.question.is_active)

    def test_get_correct_answers(self):
        """Тест получения правильных ответов"""
        correct_answers = self.question.get_correct_answers()
        self.assertEqual(len(correct_answers), 2)
        self.assertIn('-2', correct_answers)
        self.assertIn('-3', correct_answers)

    def test_check_number_answer(self):
        """Тест проверки числового ответа"""
        # Правильный ответ
        is_correct, score, feedback = self.question.check_answer(-2)
        self.assertTrue(is_correct)
        self.assertEqual(score, 2)

        # Неправильный ответ
        is_correct, score, feedback = self.question.check_answer(5)
        self.assertFalse(is_correct)
        self.assertEqual(score, 0)


class QuestionAPITest(APITestCase):
    """Тесты для API задач"""

    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

        self.subject = Subject.objects.create(title='Физика')
        self.node = Node.objects.create(
            title='Кинематика',
            subject=self.subject
        )

        self.question = Question.objects.create(
            title='Тестовая задача',
            condition='<p>Условие задачи</p>',
            question_type=QuestionType.STRING,
            max_score=1
        )
        self.question.nodes.add(self.node)

        QuestionOption.objects.create(
            question=self.question,
            text='правильный ответ',
            is_correct=True,
            order=1
        )

    def test_get_questions_list(self):
        """Тест получения списка задач"""
        response = self.client.get('/api/questions/api/questions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_get_question_detail(self):
        """Тест получения деталей задачи"""
        response = self.client.get(
            f'/api/questions/api/questions/{self.question.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Тестовая задача')

    def test_check_answer(self):
        """Тест проверки ответа"""
        response = self.client.post(
            f'/api/questions/api/questions/{self.question.id}/check_answer/',
            {'answer': 'правильный ответ'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_correct'])
        self.assertEqual(response.data['score'], 1)

    def test_create_question(self):
        """Тест создания задачи"""
        data = {
            'title': 'Новая задача',
            'condition': '<p>Условие</p>',
            'question_type': QuestionType.STRING,
            'max_score': 1,
            'options': [
                {'text': 'ответ', 'is_correct': True, 'order': 1}
            ]
        }
        response = self.client.post(
            '/api/questions/api/questions/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Question.objects.count(), 2)

    def test_copy_question(self):
        """Тест копирования задачи"""
        response = self.client.post(
            f'/api/questions/api/questions/{self.question.id}/copy/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Question.objects.count(), 2)

        # Проверяем, что копия неактивна
        copied_question = Question.objects.get(id=response.data['id'])
        self.assertFalse(copied_question.is_active)
        self.assertIn('(копия)', copied_question.title)

    def test_get_random_analog(self):
        """Тест получения случайной аналогичной задачи"""
        # Создаем аналогичную задачу
        analog_question = Question.objects.create(
            title='Аналогичная задача',
            condition='<p>Условие</p>',
            question_type=QuestionType.STRING,
            max_score=1
        )
        analog_question.nodes.add(self.node)
        QuestionOption.objects.create(
            question=analog_question,
            text='ответ',
            is_correct=True,
            order=1
        )

        # Добавляем связь
        self.question.analogs.add(analog_question)

        response = self.client.get(
            f'/api/questions/api/questions/{self.question.id}/get_random_analog/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Аналогичная задача')

    def test_random_by_node(self):
        """Тест получения случайной задачи по узлу"""
        response = self.client.get(
            f'/api/questions/api/questions/random_by_node/?node_id={self.node.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Тестовая задача')

    def test_statistics(self):
        """Тест получения статистики"""
        response = self.client.get('/api/questions/api/questions/statistics/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_questions', response.data)
        self.assertIn('by_type', response.data)
        self.assertIn('by_subject', response.data)

    def test_add_analog(self):
        """Тест добавления аналогичной задачи"""
        analog_question = Question.objects.create(
            title='Аналогичная задача',
            condition='<p>Условие</p>',
            question_type=QuestionType.STRING,
            max_score=1
        )
        QuestionOption.objects.create(
            question=analog_question,
            text='ответ',
            is_correct=True,
            order=1
        )

        response = self.client.post(
            f'/api/questions/api/questions/{self.question.id}/add_analog/',
            {'analog_id': analog_question.id}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Аналогичная задача добавлена', response.data['message'])

    def test_remove_analog(self):
        """Тест удаления аналогичной задачи"""
        analog_question = Question.objects.create(
            title='Аналогичная задача',
            condition='<p>Условие</p>',
            question_type=QuestionType.STRING,
            max_score=1
        )
        QuestionOption.objects.create(
            question=analog_question,
            text='ответ',
            is_correct=True,
            order=1
        )

        # Добавляем связь
        self.question.analogs.add(analog_question)

        response = self.client.delete(
            f'/api/questions/api/questions/{self.question.id}/remove_analog/?analog_id={analog_question.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Аналогичная задача удалена', response.data['message'])


class QuestionValidationTest(TestCase):
    """Тесты валидации задач"""

    def setUp(self):
        self.question = Question.objects.create(
            title='Тестовая задача',
            condition='<p>Условие</p>',
            question_type=QuestionType.STRING,
            max_score=1
        )

    def test_question_without_correct_options(self):
        """Тест задачи без правильных вариантов ответов"""
        with self.assertRaises(Exception):
            self.question.clean()

    def test_question_with_correct_options(self):
        """Тест задачи с правильными вариантами ответов"""
        QuestionOption.objects.create(
            question=self.question,
            text='правильный ответ',
            is_correct=True,
            order=1
        )
        # Не должно вызывать исключение
        self.question.clean()


class QuestionAnswerTest(TestCase):
    """Тесты проверки различных типов ответов"""

    def setUp(self):
        self.subject = Subject.objects.create(title='Тест')
        self.node = Node.objects.create(
            title='Тестовый узел',
            subject=self.subject
        )

    def test_string_answer(self):
        """Тест строкового ответа"""
        question = Question.objects.create(
            title='Строковая задача',
            condition='<p>Введите ответ</p>',
            question_type=QuestionType.STRING,
            max_score=1
        )
        question.nodes.add(self.node)

        QuestionOption.objects.create(
            question=question,
            text='правильный ответ',
            is_correct=True,
            order=1
        )

        is_correct, score, feedback = question.check_answer('правильный ответ')
        self.assertTrue(is_correct)
        self.assertEqual(score, 1)

        is_correct, score, feedback = question.check_answer(
            'неправильный ответ')
        self.assertFalse(is_correct)
        self.assertEqual(score, 0)

    def test_number_answer(self):
        """Тест числового ответа"""
        question = Question.objects.create(
            title='Числовая задача',
            condition='<p>Введите число</p>',
            question_type=QuestionType.NUMBER,
            max_score=2
        )
        question.nodes.add(self.node)

        QuestionOption.objects.create(
            question=question,
            text='3.14',
            is_correct=True,
            order=1
        )
        QuestionOption.objects.create(
            question=question,
            text='3.141',
            is_correct=True,
            order=2
        )

        is_correct, score, feedback = question.check_answer(3.14)
        self.assertTrue(is_correct)
        self.assertEqual(score, 2)

        is_correct, score, feedback = question.check_answer(3.141)
        self.assertTrue(is_correct)
        self.assertEqual(score, 2)

        is_correct, score, feedback = question.check_answer(3.15)
        self.assertFalse(is_correct)
        self.assertEqual(score, 0)

    def test_ordered_sequence_answer(self):
        """Тест последовательности с порядком"""
        question = Question.objects.create(
            title='Последовательность с порядком',
            condition='<p>Укажите порядок</p>',
            question_type=QuestionType.SEQUENCE_ORDERED,
            max_score=3
        )
        question.nodes.add(self.node)

        QuestionOption.objects.create(
            question=question,
            text='1,2,3',
            is_correct=True,
            order=1
        )

        is_correct, score, feedback = question.check_answer([1, 2, 3])
        self.assertTrue(is_correct)
        self.assertEqual(score, 3)

        is_correct, score, feedback = question.check_answer([3, 2, 1])
        self.assertFalse(is_correct)
        self.assertEqual(score, 0)

    def test_unordered_sequence_answer(self):
        """Тест последовательности без порядка"""
        question = Question.objects.create(
            title='Последовательность без порядка',
            condition='<p>Выберите элементы</p>',
            question_type=QuestionType.SEQUENCE_UNORDERED,
            max_score=3,
            grading_policy=GradingPolicy.ALL_OR_NOTHING
        )
        question.nodes.add(self.node)

        QuestionOption.objects.create(
            question=question,
            text='1,2,3',
            is_correct=True,
            order=1
        )
        QuestionOption.objects.create(
            question=question,
            text='3,2,1',
            is_correct=True,
            order=2
        )

        is_correct, score, feedback = question.check_answer([1, 2, 3])
        self.assertTrue(is_correct)
        self.assertEqual(score, 3)

        is_correct, score, feedback = question.check_answer([3, 2, 1])
        self.assertTrue(is_correct)
        self.assertEqual(score, 3)

        is_correct, score, feedback = question.check_answer([1, 3, 2])
        self.assertTrue(is_correct)
        self.assertEqual(score, 3)

    def test_unordered_sequence_per_error_policy(self):
        """Тест последовательности без порядка с политикой за ошибку"""
        question = Question.objects.create(
            title='Последовательность с политикой за ошибку',
            condition='<p>Выберите элементы</p>',
            question_type=QuestionType.SEQUENCE_UNORDERED,
            max_score=3,
            grading_policy=GradingPolicy.PER_ERROR
        )
        question.nodes.add(self.node)

        QuestionOption.objects.create(
            question=question,
            text='1,2,3',
            is_correct=True,
            order=1
        )

        # Правильный ответ
        is_correct, score, feedback = question.check_answer([1, 2, 3])
        self.assertTrue(is_correct)
        self.assertEqual(score, 3)

        # Частично правильный ответ (2 из 3)
        is_correct, score, feedback = question.check_answer([1, 2, 4])
        self.assertFalse(is_correct)
        self.assertEqual(score, 2)  # 2/3 * 3 = 2
