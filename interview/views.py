from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render

from core.services import GptService
from interview.models import Chat, Message, MessageRole
from job.models import Job


def create(request, job_pk):
    if request.method == "POST":
        job = get_object_or_404(Job, pk=job_pk)
        chat = Chat.objects.create(job=job)
        gpt_service = GptService()
        chat_message = gpt_service.get_chat_message(chat.messages.all())
        chat_message.chat = chat
        chat_message.save()
        return redirect("interview:details", uuid=chat.uuid)
    return HttpResponseNotAllowed(permitted_methods=["POST"])


def details(request, uuid):
    chat = get_object_or_404(Chat, uuid=uuid)
    return render(
        request,
        "interview/details.html",
        {
            "page_title": "Interview",
            "chat": chat,
        },
    )


def create_message(request, chat_uuid):
    chat = get_object_or_404(Chat, uuid=chat_uuid)
    if request.method == "POST" and not chat.completed:
        user_message = request.POST.get("answer")
        Message.objects.create(
            chat=chat,
            role=MessageRole.USER.value,
            content=user_message,
        )
        gpt_service = GptService()
        chat_message = gpt_service.get_chat_message(chat.messages.all())
        chat_message.chat = chat
        chat_message.save()
        if "feedback" in chat_message.content:
            chat.completed = True
            chat.save()
        return redirect("interview:details", uuid=chat.uuid)
    return HttpResponseNotAllowed(permitted_methods=["POST"])
