from rest_framework import serializers

from . import models


class CourseListSerializer(serializers.Serializer):

    title = serializers.CharField(read_only=True)

    cover = serializers.ImageField(read_only=True)

    rate = serializers.FloatField(read_only=True)

    category = serializers.CharField(read_only=True)

    level = serializers.CharField(read_only=True)

    teacher = serializers.StringRelatedField(read_only=True)

    price = serializers.FloatField(read_only=True)

    is_free = serializers.BooleanField(read_only=True)

    slug = serializers.SlugField(read_only=True)

    created_at = serializers.DateTimeField(read_only=True)


class CourseDetailSerializer(serializers.Serializer):

    title = serializers.CharField(read_only=True)

    overview = serializers.CharField(read_only=True)

    cover = serializers.ImageField(read_only=True)

    video = serializers.FileField(read_only=True)

    rate = serializers.FloatField(read_only=True)

    category = serializers.CharField(read_only=True)

    language = serializers.CharField(read_only=True)

    level = serializers.CharField(read_only=True)

    teacher = serializers.StringRelatedField(read_only=True)

    price = serializers.FloatField(read_only=True)

    is_free = serializers.BooleanField(read_only=True)

    created_at = serializers.DateTimeField(read_only=True)


class SectionSerializer(serializers.Serializer):

    title = serializers.CharField(read_only=True)

    order = serializers.IntegerField(read_only=True)

    slug = serializers.SlugField(read_only=True)


class QuizSerializer(serializers.Serializer):

    title = serializers.CharField(read_only=True)

    description = serializers.CharField(read_only=True)

    slug = serializers.SlugField(read_only=True)


class LectureSerializer(serializers.Serializer):

    title = serializers.CharField(read_only=True)

    slug = serializers.SlugField(read_only=True)


class LectureDetailSerializer(serializers.Serializer):

    title = serializers.CharField(read_only=True)

    text = serializers.CharField(read_only=True)

    video = serializers.FileField(read_only=True)


class AnswerSerializer(serializers.Serializer):

    text = serializers.CharField()


class QuestionSerializer(serializers.Serializer):

    question = serializers.CharField()

    choices = serializers.SerializerMethodField(read_only=True)

    def get_choices(self, obj):

        choices = AnswerSerializer(obj.answers.all(), many=True).data

        return choices


class QuizDetailSerializer(serializers.Serializer):

    title = serializers.CharField(read_only=True)

    description = serializers.CharField(read_only=True)

    questions = serializers.SerializerMethodField(read_only=True)

    def get_questions(self, obj):

        questions = QuestionSerializer(obj.questions.all(), many=True).data

        return questions
