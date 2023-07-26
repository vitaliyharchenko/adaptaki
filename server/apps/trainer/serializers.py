from rest_framework import serializers
from apps.graph.models import Subject
from apps.graph.serializers import SubjectSerializer
from .models import SubjectExam, Exam, SubjectExamNumber, ExamTag


class ExamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Exam
        fields = ['pk', 'title', 'is_active']


class ExamTagSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExamTag
        fields = ['pk', 'title', 'is_active', 'questions_exist']


class SubjectExamNumberSerializer(serializers.ModelSerializer):
    exam_tags = ExamTagSerializer(
        many=True, read_only=True)

    class Meta:
        model = SubjectExamNumber
        fields = ['pk', 'num', 'title', 'questions_exist', 'exam_tags', 'is_active']


class SubjectExamSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer()
    exam = ExamSerializer()
    subject_exam_numbers = SubjectExamNumberSerializer(
        many=True, read_only=True)

    class Meta:
        model = SubjectExam
        fields = ['pk', 'subject', 'exam',
                  'questions_exist', 'subject_exam_numbers']


class ExamTreeSerializer(serializers.ModelSerializer):
    subject_exams = SubjectExamSerializer(many=True, read_only=True)

    class Meta:
        model = Exam
        fields = ['pk', 'title', 'subject_exams', 'is_active']
