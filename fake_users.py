""" creating fake user for test"""
import os
import secrets

import django
import factory
from django.contrib.auth import get_user_model

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_playground.settings",)

django.setup()


user = get_user_model()


class UserFactory(factory.Factory):
    """
    Using factory boy to generate random data
    """

    class Meta:
        """
        Setting up the model
        """

        model = user

    email = factory.Faker(provider="email")
    password = factory.Faker(provider="password")
    username = factory.Faker(provider="user_name")
    bio = factory.Faker(provider="text")
    full_name = factory.Faker(provider="name")
    phone_num = factory.Faker(provider="phone_number")


def create_users(*, users: int = 5) -> None:
    """
    create random users
    """
    for _ in range(users):
        email = UserFactory().email
        password = UserFactory().password
        username = UserFactory().username
        bio = UserFactory().bio
        full_name = UserFactory().full_name
        phone_num = UserFactory().phone_num

        user.objects.create(
            email=email,
            bio=bio,
            full_name=full_name,
            phone_num=phone_num,
            username=username,
            gender=secrets.choice(["Female", "Male", "Rather not say"]),
            is_active=secrets.choice([True, False]),
            is_staff=secrets.choice([True, False]),
            is_superuser=secrets.choice([True, False]),
        )
        user.set_password(password)
        user.save()


create_users(users=50)
