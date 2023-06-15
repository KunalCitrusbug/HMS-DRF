"""
This file define the structure of stored data,
including the field types and possibly related information
"""

import uuid
from dataclasses import dataclass

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


@dataclass(frozen=True)
class UserID:
    """
    This is a value object that should be used to generate and pass the
    UserID to the Category
    """

    value: uuid.UUID


class UserManager(BaseUserManager):
    """
    This Following module is used to create a Custom user
    manager in order authentication with email instead of username
    """

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Enter an email address")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.is_admin = True
        user.user_type = "Admin"
        user.save(using=self._db)
        return user


class User(AbstractUser):
    """
    This Following module is for User Creation.
    Inheritance from Abstract User
    """

    USER_TYPE_CHOICE = (
        ("Patient", "Patient"),
        ("Staff", "Staff"),
        ("Admin", "Admin"),
        ("Doctor", "Doctor"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None
    email = models.EmailField("email address", unique=True)
    is_admin = models.BooleanField(default=False)
    is_forget = models.BooleanField(default=False)
    is_active = models.BooleanField(
        "active",
        default=True,
        help_text=(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    user_type = models.CharField(max_length=100, choices=USER_TYPE_CHOICE)
    entity_id = models.CharField(max_length=250, null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return str(self.email)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        db_table = "users"


class UserFactory:
    @staticmethod
    def build_entity(
            id: UserID, email: str, is_admin: bool, is_active: bool, password: str, user_type: str
    ) -> User:
        return User(
            id=id,
            email=email,
            is_admin=is_admin,
            is_active=is_active,
            password=password,
            user_type=user_type
        )

    @classmethod
    def build_entity_with_id(
            cls, email: str, is_admin: bool, is_active: bool, password: str, user_type: str
    ) -> User:
        entity_id = UserID(uuid.uuid4())
        return cls.build_entity(
            id=entity_id.value,
            email=email,
            is_admin=is_admin,
            is_active=is_active,
            password=password,
            user_type=user_type
        )
