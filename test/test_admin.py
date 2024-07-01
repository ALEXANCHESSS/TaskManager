from http import HTTPStatus
from typing import Type, Container

from django.db import models
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from main.models import Tag, Task, User
from main.models.status import Status


class TestAdmin(APITestCase):
    client: APIClient
    admin: User

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.admin = User.objects.create_superuser(
            username="test", email="test@test.ru", password="12345678"
        )

    @classmethod
    def setUp(cls):
        cls.client = APIClient()
        cls.client.force_login(cls.admin)

    @classmethod
    def assert_forms(
        cls, model: Type[models.Model], key: int, check_actions: Container = ()
    ) -> None:
        app_label = model._meta.app_label
        model_name = model._meta.model_name

        actions = {"changelist": [], "add": [], "change": (key,)}
        if check_actions:
            actions = {key: val for key, val in actions.items() if key in check_actions}

        for action, args in actions.items():
            url = reverse(f"admin:{app_label}_{model_name}_{action}", args=args)
            response = cls.client.get(url)
            assert response.status_code == HTTPStatus.OK, response.content

    def test_get_user(self) -> None:
        self.assert_forms(User, self.admin.id)

    def test_get_tag(self) -> None:
        tag = Tag.objects.create()
        self.assert_forms(Tag, tag.id)

    def test_get_task(self) -> None:
        task = Task.objects.create(author_task_id=self.admin.id)
        self.assert_forms(Task, task.id)

    def test_get_status(self) -> None:
        status = Status.objects.create()
        self.assert_forms(Status, status.id)
