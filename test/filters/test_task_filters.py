from test.base import TestViewSetBase
from test.factories import TagFactory, TaskFactory, UserFactory


class TestUserViewSet(TestViewSetBase):
    basename = "task"
    user_attributes = UserFactory

    def test_filter_title(self):
        task1 = TaskFactory.create()
        task2 = TaskFactory.create()
        task3 = TaskFactory.create()
        response = self.list({"title": task1.title})
        title = [task["title"] for task in response]

        self.assertIn(task1.title, title)
        self.assertNotIn(task2.title, title)
        self.assertNotIn(task3.title, title)

    def test_filter_status(self):
        task1 = TaskFactory.create()
        task2 = TaskFactory.create()
        task3 = TaskFactory.create()
        response = self.list({"status": task1.status.id})
        status = [task["status"] for task in response]

        self.assertIn(task1.status.id, status)
        self.assertNotIn(task2.status.id, status)
        self.assertNotIn(task3.status.id, status)

    def test_filter_tag(self):
        task1 = TaskFactory.create()
        task2 = TaskFactory.create()
        task3 = TaskFactory.create()
        tag1 = TagFactory.create()
        tag2 = TagFactory.create()
        tag3 = TagFactory.create()
        task1.tags.add(tag1)
        task2.tags.add(tag2)
        task3.tags.add(tag3)
        response = self.list({"tags": tag1.title})
        tags = [task["tags"][0] for task in response]

        self.assertIn(tag1.id, tags)
        self.assertNotIn(tag2.id, tags)
        self.assertNotIn(tag3.id, tags)

    def test_filter_author_task(self):
        task1 = TaskFactory.create()
        task2 = TaskFactory.create()
        task3 = TaskFactory.create()
        response = self.list({"author_task": task1.author_task.id})
        author_task = [task["author_task"] for task in response]

        self.assertIn(task1.author_task.id, author_task)
        self.assertNotIn(task2.author_task.id, author_task)
        self.assertNotIn(task3.author_task.id, author_task)

    def test_filter_performer_task(self):
        task1 = TaskFactory.create()
        task2 = TaskFactory.create()
        task3 = TaskFactory.create()
        response = self.list({"performer_task": task1.performer_task.id})
        performer_task = [task["performer_task"] for task in response]

        self.assertIn(task1.performer_task.id, performer_task)
        self.assertNotIn(task2.performer_task.id, performer_task)
        self.assertNotIn(task3.performer_task.id, performer_task)
