from base import faker

from test.base import TestViewSetBase
from test.factories import AdminFactory, StatusFactory, UserFactory


class TestStatusViewSet(TestViewSetBase):
    basename = "status"
    user_attributes = UserFactory

    def test_create(self):
        status_data = {
            "status": faker.word(),
        }

        self.create(status_data)

    def test_list(self):
        status = StatusFactory.create()

        response = self.list()

        assert response[0]["status"] == status.status

    def test_retrieve(self):
        status = StatusFactory.create()

        response = self.retrieve(status.id)

        assert response["status"] == status.status

    def test_update(self):
        status = StatusFactory.create()
        new_status_data = {
            "status": faker.word(),
        }

        self.update(status.id, new_status_data)

    def test_delete(self):
        status = StatusFactory.create()

        self.delete(status.id)


class TestStatusNoAuthViewSet(TestViewSetBase):
    basename = "status"
    user_attributes = None

    def test_create(self):
        status_data = {
            "status": faker.word(),
        }

        self.create(status_data)

    def test_list(self):
        StatusFactory.create()

        self.list()

    def test_retrieve(self):
        status = StatusFactory.create()

        self.retrieve(status.id)

    def test_update(self):
        status = StatusFactory.create()
        new_status_data = {
            "status": faker.word(),
        }

        self.update(status.id, new_status_data)

    def test_delete(self):
        status = StatusFactory.create()

        self.delete(status.id)


class TestStatusAdminOnlyDeleteViewSet(TestViewSetBase):
    basename = "status"
    user_attributes = AdminFactory

    def test_delete(self):
        status = StatusFactory.create()

        self.delete(status.id)
