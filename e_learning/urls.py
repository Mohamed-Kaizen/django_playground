"""blog URL Configuration"""

from django.urls import path

from .apis import rest

app_name = "e_learning"

urlpatterns = [
    path("", rest.course_list),
    path("<slug>/enroll/", rest.course_enroll),
    path(
        "<slug>/section/<section_slug>/lectures/<lecture_slug>/",
        rest.course_section_lectures,
    ),
    path(
        "<slug>/section/<section_slug>/quiz/<quiz_slug>/answer/",
        rest.course_section_quiz_answer,
    ),
    path("<slug>/section/<section_slug>/quiz/<quiz_slug>/", rest.course_section_quiz),
    path("<slug>/section/<section_slug>/", rest.course_section),
    path("<slug>/", rest.course),
]
