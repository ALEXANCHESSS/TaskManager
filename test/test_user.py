from http import HTTPStatus
from typing import Type, Container

from django.db import models
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from main.models import Tag, Task, User


class TestUser(APITestCase):
    client: APIClient
    user: User

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.user = User.objects.create(
            username="test1", email="test1@test.ru", password="12345678"
        )

    @classmethod
    def setUp(cls):
        cls.client = APIClient()
        cls.client.force_login(cls.user)

    @classmethod
    def get_assert_forms(
        cls, model: Type[models.Model], key: int, check_actions: Container = ()
    ) -> None:
        model_name = model._meta.model_name

        actions = {"list": [], "detail": (key,)}
        if check_actions:
            actions = {key: val for key, val in actions.items() if key in check_actions}

        for action, args in actions.items():
            url = reverse(f"{model_name}-{action}", args=args)
            response = cls.client.get(url)
            assert response.status_code == HTTPStatus.OK, response.content

    @classmethod
    def delete_assert_forms(cls, model: Type[models.Model], key: int) -> None:
        model_name = model._meta.model_name
        url = reverse(f"{model_name}-detail", args=[key])
        response = cls.client.delete(url)
        assert response.status_code == HTTPStatus.FORBIDDEN, response.content

    def test_get_user(self) -> None:
        self.get_assert_forms(User, self.user.id)

    def test_get_tag(self) -> None:
        tag = Tag.objects.create()
        self.get_assert_forms(Tag, tag.id)

    def test_get_task(self) -> None:
        task = Task.objects.create(author_task_id=self.user.id)
        self.get_assert_forms(Task, task.id)

    def test_delete_user(self) -> None:
        user = User.objects.create()
        self.delete_assert_forms(User, user.id)

    def test_delete_tag(self) -> None:
        tag = Tag.objects.create()
        self.delete_assert_forms(Tag, tag.id)

    def test_delete_task(self) -> None:
        task = Task.objects.create(author_task_id=self.user.id)
        self.delete_assert_forms(Task, task.id)
