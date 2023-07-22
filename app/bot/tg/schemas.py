from pydantic import BaseModel


class Chat(BaseModel):
    id: int
    username: str | None = None


class Message(BaseModel):
    chat: Chat
    text: str | None


class UpdateObj(BaseModel):
    update_id: int
    message: Message


class SendMessageResponse(BaseModel):
    ok: bool
    result: Message


class GetUpdatesResponse(BaseModel):
    ok: bool
    result: list[UpdateObj]
