import requests
from django.conf import settings

from interview.models import Message, MessageRole


class GptInsufficientQuotaError(Exception):
    ...


class GptInvalidRequestError(Exception):
    ...


class GptServiceMeta(type):
    __instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instances:
            instance = super().__call__(*args, **kwargs)
            cls.__instances[cls] = instance
        return cls.__instances[cls]


class GptService(metaclass=GptServiceMeta):
    def __init__(self):
        self.__model = settings.GPT_MODEL
        self.__open_ai_api_key = settings.OPEN_AI_API_KEY
        self.__temperature = settings.TEMPERATURE
        self.__base_url = settings.OPEN_AI_BASE_URL

    def get_chat_message(self, messages):
        payload = {
            "messages": self.__convert_to_chat_message_format(messages),
            "model": self.__model,
            "temperature": self.__temperature,
        }
        headers = {"Authorization": f"Bearer {self.__open_ai_api_key}"}
        response = requests.post(
            f"{self.__base_url}/chat/completions",
            json=payload,
            headers=headers,
        )
        body = response.json()
        if response.status_code == 429 and body["type"] == "insufficient_quota":
            raise GptInsufficientQuotaError()
        if response.status_code == 400 and body["type"] == "invalid_request_error":
            raise GptInvalidRequestError()
        message = body["choices"][0]["message"]
        return Message(role=MessageRole.ASSISTANT.value, content=message["content"])

    def __convert_to_chat_message_format(self, messages):
        return [
            {"role": message.get_role_display(), "content": message.content}
            for message in messages
        ]
