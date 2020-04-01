from typing import Dict

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from .interfaces import UserInterface
from .utils import unique_slug


def course_image_upload_to(instance: "Course", filename: str):

    return f"images/courses/{instance.title}/{filename}"


def course_video_upload_to(instance: "Course", filename: str):

    return f"videos/courses/{instance.title}/promotional/{filename}"


def lecture_video_upload_to(instance: "Lecture", filename: str):

    return f"videos/courses/{instance.section.course.title}/section/{instance.section.title}/lecture/{instance.title}/{filename}"


class Category(models.TextChoices):

    finance_accounting = ("finance_accounting", _("Finance & Accounting"))

    development = ("development", _("Development"))

    business = ("business", _("Business"))

    it_software = ("it_software", _("IT Software"))

    office_productivity = ("office_productivity", _("Office Productivity"))

    personal_development = ("personal_development", _("Personal Development"))

    design = ("design", _("Design"))

    marketing = ("marketing", _("Marketing"))

    lifestyle = ("lifestyle", _("Lifestyle"))

    photography = ("photography", _("Photography"))

    health_fitness = ("health_fitness", _("Health Fitness"))

    music = ("music", _("Music"))

    teaching_academics = ("teaching_academics", _("Teaching Academics"))


class Level(models.TextChoices):

    beginner = ("beginner", _("Beginner Level"))

    intermediate = ("intermediate", _("Intermediate Level"))

    expert = ("expert", _("Expert Level"))

    all = ("all", _("All Levels"))


class Student(models.Model):

    user = models.UUIDField(verbose_name=_("user"), unique=True)

    class Meta:
        verbose_name = _("student")
        verbose_name_plural = _("students")

    def username(self):
        return UserInterface().get_username(user_id=self.user).get("username")

    def __str__(self):
        return f"{self.username()}"


class Teacher(models.Model):

    user = models.UUIDField(verbose_name=_("user"), unique=True)

    class Meta:

        verbose_name = _("teacher")

        verbose_name_plural = _("teachers")

    def username(self):
        return UserInterface().get_username(user_id=self.user).get("username")

    def __str__(self):
        return f"{self.username()}"


class Course(models.Model):

    title = models.CharField(verbose_name=_("title"), max_length=100)

    overview = models.TextField(verbose_name=_("overview"))

    cover = models.ImageField(
        verbose_name=_("cover"), null=True, blank=True, upload_to=course_image_upload_to
    )

    video = models.FileField(
        verbose_name=_("promotional video"),
        null=True,
        blank=True,
        upload_to=course_video_upload_to,
    )

    rate = models.FloatField(verbose_name=_("rate"), blank=True, null=True, default=0)

    category = models.CharField(
        max_length=100, choices=Category.choices, verbose_name=_("category")
    )

    language = models.CharField(max_length=100, verbose_name=_("language"))

    level = models.CharField(
        max_length=100, choices=Level.choices, verbose_name=_("level")
    )

    teacher = models.ForeignKey(
        to=Teacher,
        on_delete=models.CASCADE,
        verbose_name=_("teacher"),
        db_index=True,
        related_name="courses",
    )

    student = models.ManyToManyField(
        to=Student,
        verbose_name=_("student"),
        db_index=True,
        related_name="courses",
        blank=True,
    )

    price = models.FloatField(verbose_name=_("price"))

    is_free = models.BooleanField(verbose_name=_("is it free"), default=False)

    is_drift = models.BooleanField(verbose_name=_("is it drift"), default=True)

    slug = models.SlugField(verbose_name=_("slug"), blank=True, unique=True)

    created_at = models.DateTimeField(verbose_name=_("created at"), auto_now_add=True)

    class Meta:

        verbose_name = _("course")

        verbose_name_plural = _("courses")

    def __str__(self):
        return f"{self.title}"


class Section(models.Model):

    title = models.CharField(verbose_name=_("title"), max_length=100)

    objective = models.CharField(verbose_name=_("objective"), max_length=200)

    course = models.ForeignKey(
        to=Course,
        on_delete=models.CASCADE,
        verbose_name=_("course"),
        db_index=True,
        related_name="sections",
    )

    order = models.SmallIntegerField(verbose_name=_("section order"))

    slug = models.SlugField(verbose_name=_("slug"), blank=True, unique=True)

    created_at = models.DateTimeField(verbose_name=_("created at"), auto_now_add=True)

    class Meta:

        verbose_name = _("section")

        verbose_name_plural = _("sections")

    def __str__(self):
        return f"Section {self.order}: {self.title}"


class Lecture(models.Model):

    title = models.CharField(verbose_name=_("title"), max_length=100)

    text = models.TextField(verbose_name=_("text"), null=True, blank=True)

    video = models.FileField(
        verbose_name=_("lecture video"),
        null=True,
        blank=True,
        upload_to=lecture_video_upload_to,
    )

    section = models.ForeignKey(
        to=Section,
        on_delete=models.CASCADE,
        verbose_name=_("section"),
        db_index=True,
        related_name="lectures",
    )

    slug = models.SlugField(verbose_name=_("slug"), blank=True, unique=True)

    created_at = models.DateTimeField(verbose_name=_("created at"), auto_now_add=True)

    class Meta:

        verbose_name = _("lecture")

        verbose_name_plural = _("lectures")

    def __str__(self):
        return f"{self.title}"


class Quiz(models.Model):

    title = models.CharField(verbose_name=_("title"), max_length=100)

    description = models.TextField(verbose_name=_("description"))

    section = models.ForeignKey(
        to=Section,
        on_delete=models.CASCADE,
        verbose_name=_("course"),
        db_index=True,
        related_name="quizzes",
    )

    slug = models.SlugField(verbose_name=_("slug"), blank=True, unique=True)

    created_at = models.DateTimeField(verbose_name=_("created at"), auto_now_add=True)

    class Meta:

        verbose_name = _("quiz")

        verbose_name_plural = _("quizzes")

    def __str__(self):
        return f"{self.title}"


class Question(models.Model):

    question = models.TextField(verbose_name=_("question"))

    # answer = models.CharField(verbose_name=_("answer"), max_length=700)

    quiz = models.ForeignKey(
        to=Quiz,
        on_delete=models.CASCADE,
        verbose_name=_("quiz"),
        db_index=True,
        related_name="questions",
    )

    slug = models.SlugField(verbose_name=_("slug"), blank=True, unique=True)

    created_at = models.DateTimeField(verbose_name=_("created at"), auto_now_add=True)

    class Meta:

        verbose_name = _("question")

        verbose_name_plural = _("questions")

    def __str__(self):
        return f"{self.question}"


class Answer(models.Model):

    text = models.CharField(verbose_name=_("text"), max_length=200)

    reason = models.TextField(verbose_name=_("reason"), null=True, blank=True)

    is_correct = models.BooleanField(
        verbose_name=_("is the correct answer"), default=False
    )

    question = models.ForeignKey(
        to=Question,
        on_delete=models.CASCADE,
        verbose_name=_("question"),
        db_index=True,
        related_name="answers",
    )

    class Meta:

        verbose_name = _("answer")

        verbose_name_plural = _("answers")

    def __str__(self):
        return f"{self.text} for {self.question}"


class StudentAnswer(models.Model):

    question = models.ForeignKey(
        to=Question,
        on_delete=models.CASCADE,
        verbose_name=_("question"),
        db_index=True,
        related_name="student_answer",
    )

    answer = models.ForeignKey(
        to=Answer,
        on_delete=models.CASCADE,
        verbose_name=_("answer"),
        db_index=True,
        related_name="student_answer",
    )

    student = models.ForeignKey(
        to=Student,
        on_delete=models.CASCADE,
        verbose_name=_("student"),
        db_index=True,
        related_name="student_answer",
    )

    class Meta:

        verbose_name = _("student answer")

        verbose_name_plural = _("student answers")

    def __str__(self):
        return f"{self.student} for {self.question}"

    def correct_answer(self) -> bool:

        for answer in self.question.answers.all():

            if self.answer == answer and answer.is_correct:

                return True

        return False

    correct_answer.boolean = True

    correct_answer.short_description = "Is the Correct Answer?"


@receiver(pre_save, sender=Course)
def course_slug_creator(sender: Course, instance: Course, **kwargs: Dict) -> None:

    if not instance.slug:
        instance.slug = unique_slug(title=instance.title)


@receiver(pre_save, sender=Section)
def section_slug_creator(sender: Section, instance: Section, **kwargs: Dict) -> None:

    if not instance.slug:
        instance.slug = unique_slug(title=instance.title)


@receiver(pre_save, sender=Lecture)
def lecture_slug_creator(sender: Lecture, instance: Lecture, **kwargs: Dict) -> None:

    if not instance.slug:
        instance.slug = unique_slug(title=instance.title)


@receiver(pre_save, sender=Quiz)
def quiz_slug_creator(sender: Quiz, instance: Quiz, **kwargs: Dict) -> None:

    if not instance.slug:
        instance.slug = unique_slug(title=instance.title)


@receiver(pre_save, sender=Question)
def question_slug_creator(sender: Question, instance: Question, **kwargs: Dict) -> None:

    if not instance.slug:
        instance.slug = unique_slug(title=instance.question)
