import nested_admin
from django.contrib import admin

from .models import (
    Answer,
    Course,
    Lecture,
    Question,
    Quiz,
    Section,
    Student,
    StudentAnswer,
    Teacher,
)


class AnswerInline(nested_admin.NestedStackedInline):
    model = Answer
    extra = 4


class QuestionInline(nested_admin.NestedStackedInline):
    model = Question
    inlines = [AnswerInline]
    extra = 1


class QuizInline(nested_admin.NestedStackedInline):
    model = Quiz
    inlines = [QuestionInline]
    extra = 0


class LectureInline(nested_admin.NestedStackedInline):
    model = Lecture
    extra = 0


class SectionInline(nested_admin.NestedStackedInline):
    model = Section
    inlines = [LectureInline, QuizInline]
    extra = 0
    sortable_field_name = "order"


class CourseAdmin(nested_admin.NestedModelAdmin):

    inlines = [SectionInline]

    readonly_fields = ("rate", "slug")

    list_display = (
        "title",
        "teacher",
        "level",
        "rate",
        "price",
        "category",
        "language",
        "is_free",
        "is_drift",
        "created_at",
    )

    list_filter = ("level", "category", "is_free", "is_drift", "created_at")

    search_fields = ("title", "overview")


class SectionAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "course",
        "order",
        "created_at",
    )

    list_filter = ("order", "created_at")

    search_fields = ("title", "text")


class AnswerAdmin(admin.ModelAdmin):

    list_display = (
        "text",
        "question",
        "is_correct",
    )

    list_filter = ("is_correct", "question__question")

    search_fields = ("text", "reason")


class LectureAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "section",
        "created_at",
    )

    list_filter = ("created_at", "section__title")

    search_fields = ("text", "title")


class QuestionAdmin(admin.ModelAdmin):

    list_display = (
        "question",
        "quiz",
        "created_at",
    )

    list_filter = ("created_at", "quiz__title")

    search_fields = ("question",)


class QuizAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "section",
        "created_at",
    )

    list_filter = ("created_at", "section__title")

    search_fields = ("question", "description")


class StudentAnswerAdmin(admin.ModelAdmin):

    list_display = ("student", "question", "answer", "correct_answer")


admin.site.register(Question, QuestionAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Lecture, LectureAdmin)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(StudentAnswer, StudentAnswerAdmin)
