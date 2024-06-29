from base import faker
from main.models.user import User
from test.base import TestViewSetBase
from test.factories import UserFactory


class TestUserViewSet(TestViewSetBase):
    basename = "user"
    user_attributes = UserFactory

    def test_create(self):
        user_data = {
            "username": faker.unique.user_name(),
            "email": faker.unique.email(),
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "role": User.Roles.DEVELOPER,
        }
        self.create(user_data)

    def test_list(self):
        UserFactory.create()
        self.list()

    def test_retrieve(self):
        user = UserFactory.create()
        self.retrieve(user.id)

    def test_update(self):
        user = UserFactory.create()
        new_user_data = {
            "username": faker.unique.user_name(),
            "email": faker.unique.email(),
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "role": User.Roles.DEVELOPER,
        }
        self.update(user.id, new_user_data)

    def test_delete(self):
        user = UserFactory.create()
        self.delete(user.id)


class TestUserNoAuthViewSet(TestViewSetBase):
    basename = "user"
    user_attributes = None

    def test_create(self):
        user_data = {
            "username": faker.unique.user_name(),
            "email": faker.unique.email(),
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "role": User.Roles.DEVELOPER,
        }
        self.create(user_data)

    def test_list(self):
        UserFactory.create()
        self.list()

    def test_retrieve(self):
        user = UserFactory.create()
        self.retrieve(user.id)

    def test_update(self):
        user = UserFactory.create()
        new_user_data = {
            "username": faker.unique.user_name(),
            "email": faker.unique.email(),
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "role": User.Roles.DEVELOPER,
        }
        self.update(user.id, new_user_data)

    def test_delete(self):
        user = UserFactory.create()
        self.delete(user.id)
