from rest_framework import serializers

from main.models.status import Status

from .models.tag import Tag
from .models.task import Task
from .models.user import User


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


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            "id",
            "title",
        )


class TaskReaderSerializer(serializers.ModelSerializer):
    author_task = UserSerializer()
    performer_task = UserSerializer()
    tags = TagSerializer(many=True)

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
            "tags",
        )


class TaskWriterSerializer(serializers.ModelSerializer):
    performer_task = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)

    class Meta:
        model = Task
        fields = (
            "title",
            "description",
            "date_done_before",
            "status",
            "priority",
            "performer_task",
            "tags",
        )


class TaskSerializer(serializers.ModelSerializer):
    author_task = serializers.SerializerMethodField()
    performer_task = serializers.SerializerMethodField()

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
            "tags",
        )

    def create(self, validated_data):
        validated_data["author_task"] = self.context["request"].user
        return super().create(validated_data)

    def to_representation(self, instance):
        read_serializer = TaskReaderSerializer(instance)
        return read_serializer.data

    def to_internal_value(self, data):
        write_serializer = TaskWriterSerializer(data=data)
        write_serializer.is_valid(raise_exception=True)
        return write_serializer.validated_data


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = (
            "id",
            "status",
        )
