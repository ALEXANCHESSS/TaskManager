# Generated by Django 5.0.6 on 2024-06-09 18:31

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="role",
            field=models.CharField(
                choices=[
                    ("developer", "Developer"),
                    ("manager", "Manager"),
                    ("admin", "Admin"),
                ],
                default="developer",
                max_length=255,
            ),
        ),
        migrations.CreateModel(
            name="Task",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True, null=True)),
                ("date_create", models.DateTimeField(auto_now_add=True)),
                ("date_update", models.DateTimeField(auto_now=True)),
                ("date_done_before", models.DateTimeField()),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("new_task", "New"),
                            ("in_development", "Development"),
                            ("in_qa", "Qa"),
                            ("in_code_review", "Code Review"),
                            ("ready_for_release", "Ready For Release"),
                            ("released", "Released"),
                            ("archived", "Archived"),
                        ],
                        default="new_task",
                        max_length=255,
                    ),
                ),
                (
                    "priority",
                    models.CharField(
                        choices=[
                            ("low", "Low"),
                            ("medium", "Medium"),
                            ("high", "High"),
                            ("critical", "Critical"),
                        ],
                        default="medium",
                        max_length=255,
                    ),
                ),
                (
                    "author_task",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="authored_tasks",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "performer_task",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="performer_tasks",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("task", models.ManyToManyField(related_name="tags", to="main.task")),
            ],
        ),
    ]
