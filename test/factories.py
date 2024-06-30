from datetime import datetime, timedelta, timezone
import factory

from main.models.status import Status
from main.models.tag import Tag
from main.models.task import Task
from main.models.user import User

from .base import faker


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.LazyAttribute(lambda _: faker.unique.user_name())
    password = factory.LazyAttribute(lambda _: faker.password())
    email = factory.LazyAttribute(lambda _: faker.unique.email())
    first_name = factory.LazyAttribute(lambda _: faker.unique.first_name())
    last_name = factory.LazyAttribute(lambda _: faker.unique.last_name())
    role = factory.Iterator(User.Roles)


class AdminFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.LazyAttribute(lambda _: faker.unique.user_name())
    password = factory.LazyAttribute(lambda _: faker.password())
    email = factory.LazyAttribute(lambda _: faker.unique.email())
    first_name = factory.LazyAttribute(lambda _: faker.unique.first_name())
    last_name = factory.LazyAttribute(lambda _: faker.unique.last_name())
    role = factory.Iterator(User.Roles)

    is_staff = True


class StatusFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Status

    status = factory.LazyAttribute(lambda _: faker.unique.word())


class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Task

    title = factory.LazyAttribute(lambda _: faker.sentence())
    description = factory.LazyAttribute(lambda _: faker.sentence())
    date_done_before = factory.LazyAttribute(
        lambda _: (datetime.now(timezone.utc) + timedelta(days=2)).isoformat(
            timespec="minutes"
        )
    )
    priority = factory.Iterator(Task.Priority)
    status = factory.SubFactory(StatusFactory)
    author_task = factory.SubFactory(UserFactory)
    performer_task = factory.SubFactory(UserFactory)


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tag

    title = factory.LazyAttribute(lambda _: faker.unique.word())
