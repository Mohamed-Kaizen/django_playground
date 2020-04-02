# import django.contrib.auth.password_validation as validators
from rest_framework import serializers

# from .models import CustomUser
# from .validators import (
#     validate_confusables,
#     validate_confusables_email,
#     validate_reserved_name,
# )


# class UserCreateSerializer(serializers.Serializer):
#
#     username = serializers.CharField(max_length=150)
#
#     email = serializers.EmailField()
#
#     full_name = serializers.CharField(max_length=300)
#
#     picture = serializers.ImageField(required=False)
#
#     password = serializers.CharField(style={"input_type": "password"})
#
#     def validate_username(self, username: str):
#
#         validate_reserved_name(
#             value=username, exception_class=exceptions.ValidationError
#         )
#
#         validate_confusables(value=username, exception_class=exceptions.ValidationError)
#
#         return super(UserCreateSerializer, self).validate(username)
#
#     def validate_email(self, email: str):
#
#         local_part, domain = email.split("@")
#
#         validate_reserved_name(
#             value=local_part, exception_class=exceptions.ValidationError
#         )
#
#         validate_confusables_email(
#             local_part=local_part,
#             domain=domain,
#             exception_class=exceptions.ValidationError,
#         )
#         return super(UserCreateSerializer, self).validate(email)
#
#     def validate_password(self, password: str):
#
#         validators.validate_password(password=password)
#
#         return super(UserCreateSerializer, self).validate(password)
#
#
# class UserListSerializer(serializers.Serializer):
#
#     username = serializers.CharField(max_length=150, read_only=True)
#
#     picture = serializers.ImageField(read_only=True)
#
#
# class UserChangePasswordSerializer(serializers.Serializer):
#
#     old_password = serializers.CharField(style={"input_type": "password"})
#
#     new_password = serializers.CharField(style={"input_type": "password"})
#
#     retype_new_password = serializers.CharField(style={"input_type": "password"})
#
#     def validate_new_password(self, password: str):
#
#         validators.validate_password(password=password)
#
#         return super(UserChangePasswordSerializer, self).validate(password)
#
#
# class UserRetrieveSerializer(serializers.Serializer):
#
#     username = serializers.CharField(max_length=150, read_only=True)
#
#     email = serializers.EmailField(read_only=True)
#
#     full_name = serializers.CharField(max_length=150, read_only=True)
#
#     picture = serializers.ImageField(read_only=True)
#
#
# class UserUpdateSerializer(serializers.ModelSerializer):
#
#     username = serializers.CharField(max_length=150)
#
#     email = serializers.EmailField()
#
#     full_name = serializers.CharField(max_length=150)
#
#     picture = serializers.ImageField(required=False)
#
#     class Meta:
#         model = CustomUser
#         fields = ("username", "email", "full_name", "picture")


class UserDetailsSerializer(serializers.Serializer):

    username = serializers.CharField(read_only=True)

    picture = serializers.ImageField(read_only=True)


class JWTSerializer(serializers.Serializer):

    access_token = serializers.CharField(read_only=True)

    refresh_token = serializers.CharField(read_only=True)

    user = UserDetailsSerializer(read_only=True)
