from rest_framework import serializers
from django.db import transaction

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
    performer_task = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False, allow_null=True
    )
    tags = serializers.ListField(child=serializers.CharField())

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

    @transaction.atomic
    def create(self, validated_data):
        validated_data["author_task"] = self.context["request"].user
        tags_data = validated_data.pop("tags")
        task = Task.objects.create(**validated_data)

        for tag_data in tags_data:
            tag, _ = Tag.objects.get_or_create(title=tag_data)
            task.tags.add(tag.id)

        return task

    @transaction.atomic
    def update(self, instance, validated_data):
        tags_data = validated_data.pop("tags")

        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.date_done_before = validated_data.get("date_done_before")
        instance.status = validated_data.get("status", instance.status)
        instance.priority = validated_data.get("priority", instance.priority)
        instance.performer_task = validated_data.get("performer_task")

        instance.save()

        instance.tags.clear()
        for tag_data in tags_data:
            tag, _ = Tag.objects.get_or_create(title=tag_data)
            instance.tags.add(tag.id)

        return instance

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
