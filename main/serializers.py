from rest_framework import serializers

from models.tag import Tag
from models.task import Task
from models.user import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "role",
            "date_joined",
        )


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            "id",
            "title",
            "description",
            "date_create",
            "date_update",
            "date_done_before",
            "status",
            "priority",
            "author_task",
            "performer_task",
        )

    def validate_status(self, value):
        if value not in Task.Status.values:
            raise serializers.ValidationError("Invalid status")
        return value


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            "id",
            "title",
            "task",
        )
