import django_filters

from models.tag import Tag
from models.task import Task
from models.user import User


class UserFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = User
        fields = ("name",)


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=Task.Status.choices)
    tags = django_filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(), field_name="tags__title", to_field_name="title"
    )
    author_task = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(), lookup_expr="icontains"
    )
    performer_task = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(), lookup_expr="icontains"
    )

    class Meta:
        model = Task
        fields = ("status", "tags", "author_task", "performer_task")
