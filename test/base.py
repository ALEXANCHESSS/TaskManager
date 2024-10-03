from http import HTTPStatus
from typing import Any, List, Optional, Union
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework.response import Response

from main.models.task import Task
from test.faker import faker
from test.factories import StatusFactory, UserFactory


class ActionClient:
    def __init__(self, api_client: APIClient, user) -> None:
        self.api_client = api_client
        self.user = user

    def init_user(self) -> None:
        if self.user:
            self.user = self.user.create()
            self.api_client.force_authenticate(user=self.user)

    def request_create_user(self, **attributes) -> Response:
        url = reverse("user-list")
        return self.api_client.post(url, data=attributes)  # type: ignore

    def create_user(self):
        user_attributes = UserFactory.stub().__dict__
        response = self.request_create_user(**user_attributes)
        assert response.status_code == HTTPStatus.CREATED, response.content
        return response.data

    def request_create_task(self, **attributes) -> Response:
        url = reverse("task-list")
        return self.api_client.post(url, data=attributes)  # type: ignore

    def create_task(self, **attributes) -> dict:
        user = UserFactory.create()
        status = StatusFactory.create()
        tag1 = faker.word()
        task_data = {
            "title": faker.sentence(),
            "description": faker.sentence(),
            "priority": faker.random_element(Task.Priority.values),
            "status": status.id,
            "performer_task": user.id,
            "tags": [tag1],
        }
        task_data.update(attributes)
        response = self.request_create_task(**task_data)
        assert response.status_code == HTTPStatus.CREATED, response.content
        return response.data


class TestViewSetBase(APITestCase):
    action_client: Optional[ActionClient] = None
    api_client: APIClient
    basename: str

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        # cls.user_attributes = None
        cls.api_client = APIClient()
        cls.action_client = ActionClient(cls.api_client, cls.user_attributes)
        cls.action_client.init_user()
        cls.user = cls.action_client.user

    @classmethod
    def assert_details(cls, response_data, expected_data):
        for key, value in expected_data.items():
            if key == "performer_task":
                assert response_data["performer_task"]["id"] == value, response_data[
                    "performer_task"
                ]["id"]
            elif key == "tags":
                response_tags = [tag["title"] for tag in response_data["tags"]]
                assert value == response_tags, (response_tags, value)
            else:
                assert response_data.get(key) == value, response_data.get(key)

    @classmethod
    def detail_url(cls, key: Union[int, str]) -> str:
        return reverse(f"{cls.basename}-detail", args=[key])

    @classmethod
    def list_url(cls, args: List[Union[str, int]] = None) -> str:
        return reverse(f"{cls.basename}-list", args=args)

    def request_create(
        self, data: dict, args: List[Union[str, int]] = None, **kwargs: Any
    ) -> Response:
        url = self.list_url(args)
        return self.client.post(url, data=data, **kwargs)  # type: ignore

    def list(self, data: dict = None, args: List[Union[str, int]] = None) -> dict:
        if self.user:
            self.client.force_login(self.user)
        response = self.client.get(self.list_url(args), data)
        if self.user:
            assert response.status_code == HTTPStatus.OK, response.content
        else:
            assert response.status_code == HTTPStatus.FORBIDDEN, response.content
        return response.data

    def retrieve(self, key: int) -> dict:
        if self.user:
            self.client.force_login(self.user)
        response = self.client.get(self.detail_url(key))
        if self.user:
            assert response.status_code == HTTPStatus.OK, response.content
        else:
            assert response.status_code == HTTPStatus.FORBIDDEN, response.content
        return response.data

    def create(
        self, data: dict, args: List[Union[str, int]] = None, **kwargs: Any
    ) -> dict:
        if self.user:
            self.client.force_login(self.user)
        response = self.request_create(data, args, **kwargs)
        if self.user:
            self.assert_details(response.data, data)
            assert response.status_code == HTTPStatus.CREATED, response.content
        else:
            assert response.status_code == HTTPStatus.FORBIDDEN, response.content
        return response.data

    def update(self, key: int, data: dict) -> dict:
        if self.user:
            self.client.force_login(self.user)
        response = self.client.put(self.detail_url(key), data=data)
        if self.user:
            self.assert_details(response.data, data)
            assert response.status_code == HTTPStatus.OK, response.content
        else:
            assert response.status_code == HTTPStatus.FORBIDDEN, response.content
        return response.data

    def delete(self, key: int) -> dict:
        if self.user:
            self.client.force_login(self.user)
        response = self.client.delete(self.detail_url(key))

        if self.user and self.user.is_staff:
            assert response.status_code == HTTPStatus.NO_CONTENT, response.content
        else:
            assert response.status_code == HTTPStatus.FORBIDDEN, response.content
        return response.data
