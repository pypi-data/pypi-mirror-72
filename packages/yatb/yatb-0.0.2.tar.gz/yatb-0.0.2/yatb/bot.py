from enum import Enum
from typing import Union

import attr
import httpx
import ujson

from . import exceptions, types


class Action(str, Enum):
    """
    Enum of supported Telegram actions (methods)
    """

    get_me = "getMe"
    send_message = "sendMessage"


@attr.s
class BaseBot:
    """
    Base class for Telegram Bot object.
    Sync and async Bot versions are derived from this class
    """

    token: str = attr.ib()
    client: Union[httpx.Client, httpx.AsyncClient] = attr.ib()
    telegram_url: str = attr.ib(default="https://api.telegram.org")

    def get_me(self):
        raise NotImplementedError

    def __attrs_post_init__(self):
        self.telegram_url = self.telegram_url.rstrip("/")

    def _get_url(self, action: Action):
        return f"{self.telegram_url}/bot{self.token}/{action.value}"

    def _send(self, request: httpx.Request) -> dict:
        response = self.client.send(request)
        response.raise_for_status()

        response_data = ujson.loads(response.content)
        if response_data["ok"] is False:
            raise exceptions.TelegramAPIException(response.content)

        return response_data["result"]

    async def _asend(self, request: httpx.Request) -> dict:
        response = await self.client.send(request)
        response.raise_for_status()

        response_data = ujson.loads(response.content)
        if response_data["ok"] is False:
            raise exceptions.TelegramAPIException(response.content)

        return response_data["result"]

    def _build_get_me_request(self) -> httpx.Request:
        return self.client.build_request("GET", self._get_url(Action.get_me),)

    def _build_send_message_request(
        self, chat_id: Union[str, int], text: str
    ) -> httpx.Request:
        return self.client.build_request(
            "POST",
            self._get_url(Action.send_message),
            data={"chat_id": chat_id, "text": text},
        )


class AsyncBot(BaseBot):
    """
    Asynchronous Telegram Bot
    """

    client: httpx.AsyncClient = attr.ib()

    async def get_me(self) -> types.User:
        """
        A simple method for testing your bot's auth token. Requires no parameters.
        Returns basic information about the bot in form of a User object.

        https://core.telegram.org/bots/api#getme
        """
        data = await self._asend(self._build_get_me_request())
        return types.User(**data)

    # todo: add support for the remaining options
    async def send_message(self, chat_id: Union[str, int], text: str,) -> types.Message:
        """
        Use this method to send text messages.
        On success, the sent Message is returned.

        https://core.telegram.org/bots/api#sendmessage
        """
        data = await self._asend(
            self._build_send_message_request(chat_id=chat_id, text=text)
        )
        return types.Message(**data)
