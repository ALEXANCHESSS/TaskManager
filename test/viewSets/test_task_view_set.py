from test.faker import faker
from main.models.task import Task
from test.base import TestViewSetBase
from test.factories import (
    AdminFactory,
    StatusFactory,
    TaskFactory,
    UserFactory,
)


class TestTaskViewSet(TestViewSetBase):
    basename = "task"
    user_attributes = UserFactory

    def test_create(self):
        user = UserFactory.create()
        status = StatusFactory.create()
        tag1, tag2 = faker.word(), faker.word()
        task_data = {
            "title": faker.sentence(),
            "description": faker.sentence(),
            "priority": faker.random_element(Task.Priority.values),
            "status": status.id,
            "performer_task": user.id,
            "tags": [tag1, tag2],
        }
        self.create(task_data, format="json")

    def test_list(self):
        task = TaskFactory.create()

        response = self.list()

        assert response[0]["title"] == task.title

    def test_retrieve(self):
        task = TaskFactory.create()

        response = self.retrieve(task.id)

        assert response["title"] == task.title

    def test_update(self):
        user = UserFactory.create()
        task = TaskFactory.create()
        status = StatusFactory.create()
        tag = faker.word()
        new_task_data = {
            "title": faker.sentence(),
            "description": faker.sentence(),
            "priority": faker.random_element(Task.Priority.values),
            "status": status.id,
            "performer_task": user.id,
            "tags": [tag],
        }

        self.update(task.id, new_task_data)

    def test_delete(self):
        task = TaskFactory.create()

        self.delete(task.id)


class TestTaskNoAuthViewSet(TestViewSetBase):
    basename = "task"
    user_attributes = None

    def test_create(self):
        user = UserFactory.create()
        status = StatusFactory.create()
        task_data = {
            "title": faker.sentence(),
            "description": faker.sentence(),
            "priority": faker.random_element(Task.Priority.values),
            "status": status.id,
            "performer_task": user.id,
        }

        self.create(task_data)

    def test_list(self):
        TaskFactory.create()

        self.list()

    def test_retrieve(self):
        task = TaskFactory.create()

        self.retrieve(task.id)

    def test_update(self):
        user = UserFactory.create()
        task = TaskFactory.create()
        status = StatusFactory.create()
        new_task_data = {
            "title": faker.sentence(),
            "description": faker.sentence(),
            "priority": faker.random_element(Task.Priority.values),
            "status": status.id,
            "performer_task": user.id,
        }

        self.update(task.id, new_task_data)

    def test_delete(self):
        task = TaskFactory.create()

        self.delete(task.id)


class TestTaskAdminOnlyDeleteViewSet(TestViewSetBase):
    basename = "task"
    user_attributes = AdminFactory

    def test_delete(self):
        task = TaskFactory.create()

        self.delete(task.id)
