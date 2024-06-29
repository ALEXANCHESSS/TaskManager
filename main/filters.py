import django_filters

from .models.status import Status
from .models.tag import Tag
from .models.task import Task
from .models.user import User


class UserFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(lookup_expr="icontains")
    last_name = django_filters.CharFilter(lookup_expr="icontains")
    username = django_filters.CharFilter(lookup_expr="icontains")
    role = django_filters.CharFilter(lookup_expr="exact")

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "role")


class TaskFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr="icontains")
    status = django_filters.ModelChoiceFilter(queryset=Status.objects.all())
    tags = django_filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(), field_name="tags__title", to_field_name="title"
    )
    author_task = django_filters.ModelChoiceFilter(queryset=User.objects.all())
    performer_task = django_filters.ModelChoiceFilter(queryset=User.objects.all())

    class Meta:
        model = Task
        fields = ("title", "status", "tags", "author_task", "performer_task")
