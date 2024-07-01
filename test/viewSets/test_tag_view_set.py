from base import faker

from test.base import TestViewSetBase
from test.factories import AdminFactory, TagFactory, UserFactory


class TestTagViewSet(TestViewSetBase):
    basename = "tag"
    user_attributes = UserFactory

    def test_create(self):
        tag_data = {
            "title": faker.sentence(),
        }

        self.create(tag_data)

    def test_list(self):
        tag = TagFactory.create()

        response = self.list()

        assert response[0]["title"] == tag.title

    def test_retrieve(self):
        tag = TagFactory.create()

        response = self.retrieve(tag.id)

        assert response["title"] == tag.title

    def test_update(self):
        tag = TagFactory.create()
        new_tag_data = {
            "title": faker.sentence(),
        }

        self.update(tag.id, new_tag_data)

    def test_delete(self):
        tag = TagFactory.create()

        self.delete(tag.id)


class TestTagNoAuthViewSet(TestViewSetBase):
    basename = "tag"
    user_attributes = None

    def test_create(self):
        tag_data = {
            "title": faker.sentence(),
        }

        self.create(tag_data)

    def test_list(self):
        TagFactory.create()

        self.list()

    def test_retrieve(self):
        tag = TagFactory.create()

        self.retrieve(tag.id)

    def test_update(self):
        tag = TagFactory.create()
        new_tag_data = {
            "title": faker.sentence(),
        }

        self.update(tag.id, new_tag_data)

    def test_delete(self):
        tag = TagFactory.create()

        self.delete(tag.id)


class TestTagAdminOnlyDeleteViewSet(TestViewSetBase):
    basename = "tag"
    user_attributes = AdminFactory

    def test_delete(self):
        tag = TagFactory.create()

        self.delete(tag.id)