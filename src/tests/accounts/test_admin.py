from tests.base import BaseTest


class AdminUserTests(BaseTest):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        client = cls.client

    def test_create_user(self):
        print("test passed")
