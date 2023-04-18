import uuid
from enum import Enum
from functools import reduce

from django.conf import settings
from django.db import models
from django.urls import reverse


class MessageRole(Enum):
    SYSTEM = "system"
    ASSISTANT = "assistant"
    USER = "user"

    @classmethod
    def choices(cls):
        return [(key.value, key.value) for key in cls]


class Message(models.Model):
    chat = models.ForeignKey(
        "interview.Chat", on_delete=models.CASCADE, related_name="messages"
    )
    role = models.CharField(max_length=10, choices=MessageRole.choices())
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.role} - {self.chat.title}"


class Chat(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False)
    title = models.CharField(max_length=100, editable=False)
    job = models.ForeignKey("job.Job", on_delete=models.CASCADE, related_name="chats")
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid4()
            self.title = f"Chat {self.job.title} - {self.uuid}"
            super().save(*args, **kwargs)
            replaces = {
                "{job_title}": self.job.title,
                "{job_requirements}": self.job.requirements,
                "{job_responsibilities}": self.job.responsibilities,
            }
            initial_prompt = reduce(
                lambda acc, key: acc.replace(key, replaces[key]),
                replaces,
                settings.INITIAL_PROMPT_TEMPLATE,
            )
            Message.objects.create(
                chat=self, role=MessageRole.SYSTEM.value, content=initial_prompt
            )
        else:
            super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("interview:details", kwargs={"uuid": self.uuid})
