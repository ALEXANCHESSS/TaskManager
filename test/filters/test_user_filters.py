from main.models.user import User
from test.base import TestViewSetBase
from test.factories import UserFactory


class TestUserViewSet(TestViewSetBase):
    basename = "user"
    user_attributes = UserFactory

    def test_filter_role(self):
        UserFactory.create(role=User.Roles.ADMIN)
        UserFactory.create(role=User.Roles.DEVELOPER)
        UserFactory.create(role=User.Roles.MANAGER)

        response = self.list({"role": User.Roles.DEVELOPER})
        roles = [user["role"] for user in response]

        assert User.Roles.DEVELOPER in roles
        assert User.Roles.ADMIN not in roles
        assert User.Roles.MANAGER not in roles

    def test_filter_first_name(self):
        user1 = UserFactory.create()
        user2 = UserFactory.create()
        user3 = UserFactory.create()

        response = self.list({"first_name": user1.first_name})
        first_name = [user["first_name"] for user in response]

        assert user1.first_name in first_name
        assert user2.first_name not in first_name
        assert user3.first_name not in first_name

    def test_filter_last_name(self):
        user1 = UserFactory.create()
        user2 = UserFactory.create()
        user3 = UserFactory.create()

        response = self.list({"last_name": user1.last_name})
        last_name = [user["last_name"] for user in response]

        assert user1.last_name in last_name
        assert user2.last_name not in last_name
        assert user3.last_name not in last_name

    def test_filter_username(self):
        user1 = UserFactory.create()
        user2 = UserFactory.create()
        user3 = UserFactory.create()

        response = self.list({"username": user1.username})
        username = [user["username"] for user in response]

        assert user1.username in username
        assert user2.username not in username
        assert user3.username not in username
