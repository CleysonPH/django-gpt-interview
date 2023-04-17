from django.contrib import admin

from interview.models import Chat, Message


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ("title", "job", "completed")
    list_filter = ("completed",)
    inlines = (MessageInline,)
