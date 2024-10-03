from doctest import debug
from unittest.mock import patch, MagicMock

from django.core import mail
from django.template.loader import render_to_string

from main.models import Task
from main.services.mail import send_assign_notification
from test.base import TestViewSetBase
from test.factories import UserFactory


class TestSendEmail(TestViewSetBase):
    user_attributes = UserFactory

    @patch.object(mail, "send_mail")
    def test_send_assign_notification(self, mock_sender: MagicMock) -> None:
        assignee = self.action_client.create_user()
        task = self.action_client.create_task(performer_task=assignee["id"])

        send_assign_notification(task["id"])

        mock_sender.assert_called_once_with(
            subject="You've assigned a task.",
            message="",
            from_email=None,
            recipient_list=[assignee["email"]],
            html_message=render_to_string(
                "emails/notification.html",
                context={"task": Task.objects.get(pk=task["id"])},
            ),
        )
