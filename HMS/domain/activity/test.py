# """
# This following file is document, which has set of
#     Test data,
#     Pre-Conditions,
#     Expected results,
#     Post-Conditions
# developed for particular module and for code coverage
# """
# import datetime
#
# from django.test import TestCase
#
#
#
# # [NOTE] - This module is an activity tracking module that tracks activity records for each module.
# #          This module will be used as an AbstractModel, so we will test it using a submodule from the following module.
#
#
# class TestActivity(TestCase):
#     """
#     This following file contains test-cases
#     to check code functionality and code coverage.
#     """
#
#     @classmethod
#     def setUpClass(cls) -> None:
#         cls.activity_factory = ActivityFactory()
#         cls.activity_service = ActivityServices()
#         cls.category_factory = CategoryFactory()
#         cls.category_service = CategoryServices()
#         return super().setUpClass()
#
#     def test_get_factory_method(self):
#         try:
#             self.activity_factory.build_entity
#             self.activity_factory.build_entity_with_id
#             self.assertTrue(True)
#         except Exception as e:
#             self.fail(f"Unexpected failure: {e}")
#
#     def test_category_activity_with_build_entity_with_id(self):
#         try:
#             category_activity_obj = (
#                 self.category_service.get_category_factory().build_entity_with_id(
#                     title="test_category",
#                     created_at=datetime.datetime.now(),
#                 )
#             )
#         except Exception as e:
#             self.fail(f"Unexpected failure: {e}")
