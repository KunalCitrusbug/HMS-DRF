"""
This following file contains all queries related to particular model.
"""

from typing import Type

from django.db.models.manager import BaseManager

from HMS.domain.activity.models import Activity, ActivityFactory


class ActivityServices:
    """
    This creates model service that provide abstract layer over
    model and user have to access service layer instead of accessing model.
    """

    def get_activity_factory(
            self,
    ) -> Type[ActivityFactory]:
        return ActivityFactory

    def get_activity_repo(self) -> BaseManager[Activity]:
        return Activity.objects

    @staticmethod
    def get_activity_by_id(activity_id: str) -> Type[Activity]:
        return Activity.objects.get(id=activity_id)
