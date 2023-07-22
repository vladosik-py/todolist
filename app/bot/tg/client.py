from typing import Any
import requests
from pydantic import ValidationError

from bot.tg.schemas import GetUpdatesResponse, SendMessageResponse
from todolist import settings


class TgClient:
    def __int__(self, token: str | None = None) -> None:
        self.__token = token if token else settings.BOT_TOKEN
        self.__base_url = f'https://api.telegram.org/bot{self.__token}/'

    def get_updates(self, offset: int = 0, timeout: int = 60) -> GetUpdatesResponse:
        data = self._get('getUpdates', offset=offset, timeout=timeout)
        return GetUpdatesResponse(**data)

    def send_message(self, chat_id: int, text: str) -> SendMessageResponse:
        data = self._get('sendMessage', chat_id=chat_id, text=text)
        return SendMessageResponse(**data)

    def __get_url(self, method: str) -> str:
        return f'{self.__base_url}{method}'

    def _get(self, command: str, **params: Any) -> dict:
        url = self.__get_url(command)
        response = requests.get(url, params=params)
        if not response.ok:
            print(f'Invalid status code from telegram {response.status_code} on command {command}')
            return {'ok': False, 'result': []}
        return response.json()


def _serialize_response(serializer_class, data):
    try:
        return serializer_class(**data)
    except ValidationError as e:
        print(f'Failed to serialize telegram response due {e}')
        raise ValueError