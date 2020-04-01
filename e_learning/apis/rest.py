from typing import Dict

from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from .. import models, serializers


@api_view(["GET"])
def course_list(request: Request) -> Response:

    courses = models.Course.objects.filter(is_drift=False).order_by("-rate")

    serializer = serializers.CourseListSerializer(courses, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def course(request: Request, slug: str) -> Response:

    course = models.Course.objects.get(slug=slug)

    serializer = serializers.CourseDetailSerializer(course)

    data = serializer.data

    data.update({"has_toke_the course": False})

    if request.user.is_authenticated and course.student.filter(
        user=request.user.user_uuid
    ):

        data.update({"has_toke_the course": True})

        section_serializer = serializers.SectionSerializer(
            course.sections.all(), many=True
        )

        data.update({"sections": section_serializer.data})

    return Response(data)


@api_view(["Post"])
def course_enroll(request: Request, slug: str) -> Response:

    user = request.user

    student = models.Student.objects.filter(user=user.user_uuid)

    if student:

        course = models.Course.objects.get(slug=slug)

        students_course = course.student.filter(user=user.user_uuid)

        if not students_course:

            if course.is_free:

                course.student.add(student.first())

                course.save()

                return Response({"A": "OK"})

            else:

                return Response({"A": "you need to pay"})

        return Response({"A": "you can't"})

    return Response({"A": "you are not student"})


@api_view(["GET"])
def course_section(request: Request, section_slug: str, **kwargs: Dict) -> Response:

    section = models.Section.objects.get(slug=section_slug)

    data = {"title": f"{section.title}", "objective": f"{section.objective}"}

    quizzes = section.quizzes.all()

    lectures = section.lectures.all()

    if lectures:

        lecture_serializer = serializers.LectureSerializer(lectures, many=True)

        data.update({"lectures": lecture_serializer.data})

    if quizzes:

        quiz_serializer = serializers.QuizSerializer(quizzes, many=True)

        data.update({"quizzes": quiz_serializer.data})

    return Response(data)


@api_view(["GET"])
def course_section_lectures(
    request: Request, lecture_slug: str, **kwargs: Dict
) -> Response:

    lecture = models.Lecture.objects.get(slug=lecture_slug)

    serializer = serializers.LectureDetailSerializer(lecture)

    return Response(serializer.data)


@api_view(["GET"])
def course_section_quiz(request: Request, quiz_slug: str, **kwargs: Dict) -> Response:

    quiz = models.Quiz.objects.get(slug=quiz_slug)

    print(quiz.questions.all())

    serializer = serializers.QuizDetailSerializer(quiz)

    return Response(serializer.data)


@api_view(["POST"])
def course_section_quiz_answer(
    request: Request, quiz_slug: str, **kwargs: Dict
) -> Response:

    # {"questions": [{"question": "python have", "answer": "import keyword"}, {"question": "asdasdasd", "answer": "hhhhhhhhhhh"}]}

    quiz = models.Quiz.objects.get(slug=quiz_slug)

    for question in request.data.get("questions"):

        selected_question = quiz.questions.get(question=question.get("question"))

        selected_answer = selected_question.answers.get(text=question.get("answer"))
        selected_student = models.Student.objects.get(user=request.user.user_uuid)
        student_answer = models.StudentAnswer(
            question=selected_question, answer=selected_answer, student=selected_student
        )
        student_answer.save()
        print(selected_question)

        print(selected_answer)

    return Response({"d": "S"})
