from http import HTTPStatus
from faker import Faker
from typing import Any, List, Union
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework.response import Response

from main.models.user import User


faker = Faker()


class TestViewSetBase(APITestCase):
    user: User
    client: APIClient
    basename: str

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.user = cls.create_api_user()
        cls.client = APIClient()

    @classmethod
    def create_api_user(cls) -> User:
        if cls.user_attributes:
            return cls.user_attributes.create()

    @classmethod
    def assert_details(cls, response_data, expected_data):
        for key, value in expected_data.items():
            assert response_data.get(key) == value

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
        if self.user:
            assert response.status_code == HTTPStatus.FORBIDDEN, response.content
        else:
            assert response.status_code == HTTPStatus.FORBIDDEN, response.content
        return response.data
