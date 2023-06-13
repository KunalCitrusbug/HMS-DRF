"""
This file define the structure of stored data,
including the field types and possibly related information
"""

import uuid
from dataclasses import dataclass
from datetime import datetime

from django.db import models


@dataclass(frozen=True)
class ActivityID:
    """
    This is a value object that should be used to generate and pass the
    ActivityID to the Category
    """

    value: uuid.UUID


class Activity(models.Model):
    """
    This module will contain activity records of each module.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        verbose_name = "Activity"
        verbose_name_plural = "Activities"
        db_table = "activity"


class ActivityFactory:
    @staticmethod
    def build_entity(
        id: ActivityID, created_at: datetime, updated_at: datetime
    ) -> Activity:
        return Activity(id=id, created_at=created_at, updated_at=updated_at)

    @classmethod
    def build_entity_with_id(
        cls, created_at: datetime, updated_at: datetime
    ) -> Activity:
        entity_id = ActivityID(uuid.uuid4())
        return cls.build_entity(
            id=entity_id.value, created_at=created_at, updated_at=updated_at
        )
